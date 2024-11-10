from django.contrib import admin

from .models import (
    Category,
    Step,
    StepFile,
    StepTest,
    Subject,
    TestAnswer,
    TestQuestion,
    UserStep,
    UserSubject,
    UserTestResult,
    UserTotalTestResult,
)

admin.site.register(TestQuestion)
admin.site.register(TestAnswer)
admin.site.register(UserTotalTestResult)


class SubjectInline(admin.StackedInline):
    model = Subject
    extra = 1
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "click_count")
    inlines = [SubjectInline]


class StepInlineAdmin(admin.StackedInline):
    model = Step
    extra = 1


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    inlines = [StepInlineAdmin]


@admin.register(UserSubject)
class UserSubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "user")


@admin.register(StepFile)
class StepFileAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


class StepFileInlineAdmin(admin.StackedInline):
    model = StepFile
    extra = 1


@admin.register(UserStep)
class UserStepAdmin(admin.ModelAdmin):
    list_display = ("id", "user")


@admin.register(StepTest)
class StepTestAdmin(admin.ModelAdmin):
    pass


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    inlines = [StepFileInlineAdmin]
