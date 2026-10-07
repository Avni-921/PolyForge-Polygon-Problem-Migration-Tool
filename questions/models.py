from django.db import models


class CodeforcesQuestion(models.Model):
    """Stores a Codeforces problem for display in the demo dashboard."""

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    title = models.CharField(max_length=255)
    url = models.URLField(help_text="Direct link to the Codeforces problem")
    statement = models.TextField(help_text="Brief problem description")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags e.g. math,greedy")

    @property
    def tags_list(self):
        """Split the comma-separated tags string into a Python list.
        Used in templates as {{ q.tags_list }} — no method call needed."""
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    def __str__(self):
        return self.title
