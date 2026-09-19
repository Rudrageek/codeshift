from dataclasses import dataclass


@dataclass
class SourceEdit:
    """
    Represents a modification to source code.

    start:
        Starting character offset.

    end:
        Ending character offset.

    replacement:
        Text that replaces source[start:end].
    """

    start: int
    end: int
    replacement: str


def apply_edits(
    source_code: str,
    edits: list[SourceEdit],
) -> str:
    """
    Apply source edits safely.

    Edits are applied from right to left so that
    earlier offsets are not affected by later edits.
    """

    if not edits:
        return source_code

    # Apply edits from the end of the file toward
    # the beginning.
    sorted_edits = sorted(
        edits,
        key=lambda edit: edit.start,
        reverse=True,
    )

    result = source_code

    previous_start = len(source_code) + 1

    for edit in sorted_edits:

        # ---------------------------------
        # Validate edit range
        # ---------------------------------

        if edit.start < 0:
            raise ValueError(
                "Edit start cannot be negative."
            )

        if edit.end < edit.start:
            raise ValueError(
                "Edit end cannot be before edit start."
            )

        if edit.end > len(source_code):
            raise ValueError(
                "Edit end is outside source code."
            )

        # ---------------------------------
        # Prevent overlapping edits
        # ---------------------------------

        if edit.end > previous_start:
            raise ValueError(
                "Source edits cannot overlap."
            )

        # ---------------------------------
        # Apply edit
        # ---------------------------------

        result = (
            result[:edit.start]
            + edit.replacement
            + result[edit.end:]
        )

        previous_start = edit.start

    return result