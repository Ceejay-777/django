from .permissions import IsStaffEditorPermission
from rest_framework import permissions

class StaffEditorPermissionMixin():
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]
    
class UserQuerySetMixin():
    user_field = 'user'
    def get_queryset(self, *args, **kwargs):
        lookup_data = {}
        user = self.request.user
        lookup_data[self.user_field] = user
        queryset = super().get_queryset(*args, **kwargs)
        if user.is_staff:
            return queryset
        return queryset.filter(**lookup_data)