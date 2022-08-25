#

# ��������� �������
STATE_ACCESS_DENIED       = -1            # ������� �� �������� (���. � ��)
STATE_COOLDOWN            = 0             # ������� �� ������
STATE_LIMIT               = 1             # ��������� ����� �� �������������
STATE_OVERLIMIT           = 2             # ���-�� ���. ������ ������� ������
STATE_READY               = 3             # ������� ��������

# ======== ========= ========= ========= ========= ========= ========= =========

# ���������� � ��������� ������� ���������� �������
class ICommandState:
    def new_state(self, node, now):
        pass

    def state(self, now):
        pass

    @property
    def name(self):
        return ""

    def update(self, expired):
        pass

    async def search(self, ctx):
        pass

# ======== ========= ========= ========= ========= ========= ========= =========

class CommandState(ICommandState):
    def __init__(self, node, now):
        self._node      = node         # ������� ICommandNode
        self._count     = 0            # ���������� ������������� �������
        self._prev      = 0            # ����� �������������� ������
        self._last      = now          # ����� ���������� ������

    def new_state(self, node, now):
        if self._node.name != node.name:
            self._count = 0
            self._last  = now

        self._prev      = self._last
        self._node      = node
        self._last      = now
        self._count    += 1

    def state(self, now):
        if self._node.limit:
            if self._count == self._node.limit+1:
                return STATE_LIMIT
            elif self._count > self._node.limit+1:
                return STATE_OVERLIMIT
        if (not self._node.limit and now != self._prev) or \
           (self._node.limit and now != self._last):       # ������ ��� ��������
            if self._node.cooldown and now < self._prev + self._node.cooldown:
                return STATE_COOLDOWN
        return STATE_READY

    # expired - �������� �� ������ ���������� ��������
    # expired = now-remember_time �� ���������: now < last+remember_time
    def update(self, expired):
        # ���� ������ False, �� ��������� ����� �������. ������������ ������
        return expired < self._last

    @property
    def name(self):
        return self._node.name

    async def search(self, ctx):
        node = await self._node.check(ctx)
        if node is None and self._count:
            node = await self._node.find(ctx)
        return node

# ======== ========= ========= ========= ========= ========= ========= =========