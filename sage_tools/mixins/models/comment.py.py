from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class CommentBaseModel(models.Model):
    """
    An abstract base class model that provides a common structure for comments across different models.
    This mixin includes fields for associating a comment with a user, storing the comment's message,
    and supporting nested replies to facilitate threaded discussions.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="comments",
        verbose_name=_("User"),
        help_text=_(
            "Select the user who submitted this comment or question. If the user is deleted, the "
            "comment will remain but the user reference will be removed."
        ),
        db_comment="User who submitted the comment or question.",
    )

    message = models.TextField(
        verbose_name=_("Comment Message"),
        help_text=_("Enter the comment, feedback, or question provided by the user."),
        db_comment="Text comment/question submitted by the user.",
    )

    reply = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
        verbose_name=_("Parent Comment"),
        help_text=_(
            "The parent comment to which this is a reply. Leave this blank for top-level comments."
        ),
        db_comment="Parent comment this is a reply to.",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_(
            "Indicates whether the comment is active and visible on the site. Use this to hide comments that violate site policies."
        ),
        db_comment="Flag to indicate if the comment is active and should be displayed.",
    )

    class Meta:
        abstract = True
