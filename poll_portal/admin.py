from django.contrib import admin
from .models import Poll, Vote


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'result_published', 'total', 'pub_date', 'created_by')
    list_filter = ('is_active', 'result_published', 'pub_date')
    search_fields = ('question',)
    readonly_fields = ('option_one_count', 'option_two_count', 'option_three_count', 'pub_date')
    actions = ['publish_results', 'unpublish_results', 'close_polls', 'open_polls']

    def publish_results(self, request, queryset):
        queryset.update(result_published=True)
        self.message_user(request, 'Selected poll results have been published.')
    publish_results.short_description = 'Publish results for selected polls'

    def unpublish_results(self, request, queryset):
        queryset.update(result_published=False)
        self.message_user(request, 'Selected poll results have been unpublished.')
    unpublish_results.short_description = 'Unpublish results for selected polls'

    def close_polls(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, 'Selected polls have been closed.')
    close_polls.short_description = 'Close selected polls'

    def open_polls(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, 'Selected polls have been opened.')
    open_polls.short_description = 'Open selected polls'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'poll', 'choice', 'voted_on')
    list_filter = ('poll', 'choice', 'voted_on')
    search_fields = ('user__username', 'poll__question')
    readonly_fields = ('user', 'poll', 'choice', 'voted_on')
