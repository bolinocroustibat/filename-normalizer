from utils.logger import FileLogger


def print_summary(
    renamed_count: int,
    skipped_count: int,
    already_correct: int,
    total_files: int,
) -> None:
    """Print a summary of the renaming operations."""
    logger = FileLogger("summary")
    logger.info("\nSummary:")
    logger.info(f"Files already in correct format: {already_correct}")
    logger.success(f"Files renamed: {renamed_count}")
    logger.warning(f"Files skipped: {skipped_count}")
    logger.info(f"Total files processed: {total_files}")
