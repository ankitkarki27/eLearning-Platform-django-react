from rest_framework import serializers
from .models import TeamMember

class TeamMemberSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = TeamMember
        fields = [
            'id',
            'full_name',
            'email',
            'role',
            'working_status',
            'work_type',
            'bio',
            'profile_image',
            'date_of_birth',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']
