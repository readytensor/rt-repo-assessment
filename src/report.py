import os
from typing import Dict, List, Any


def generate_markdown_report(
    assessment: Dict[str, Any],
    output_file: str,
    criteria_categories: Dict[str, List[str]],
    criteria_names: Dict[str, str],
    category_criteria: Dict[str, List[str]],
):
    """
    Generate a Markdown report summarizing criteria satisfaction.

    Args:
        assessment: Dictionary containing assessment results with criteria IDs as keys
        output_file: Path where to save the Markdown report
        criteria_categories: Dictionary mapping category names to lists of criteria IDs
        criteria_names: Dictionary mapping criteria IDs to their display names
        category_criteria: Dictionary mapping category names to lists of criteria IDs
    """

    total_criteria = len(assessment)
    met_criteria = sum(1 for score in assessment.values() if score.get("score", 0) == 1)

    # Calculate statistics by category
    category_stats = {}
    for category, criteria_list in criteria_categories.items():
        # Only count criteria that exist in the assessment
        criteria_in_assessment = [crit for crit in criteria_list if crit in assessment]
        total_in_category = len(criteria_in_assessment)
        met_in_category = sum(
            1
            for crit in criteria_in_assessment
            if assessment[crit].get("score", 0) == 1
        )
        category_stats[category] = {
            "total": total_in_category,
            "met": met_in_category,
            "percentage": (
                round(met_in_category / total_in_category * 100, 1)
                if total_in_category > 0
                else 0
            ),
        }

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate Markdown report
    with open(output_file, "w") as f:
        f.write("# Code Quality Assessment Report\n\n")

        # Overall summary
        f.write("## Overall Summary\n\n")
        f.write(f"- **Total Criteria**: {total_criteria}\n")
        f.write(
            f"- **Criteria Met**: {met_criteria} ({round(met_criteria/total_criteria*100, 1)}%)\n\n"
        )

        # Category breakdown
        f.write("## Category Breakdown\n\n")
        f.write("| Category | Criteria Met | Total Criteria | Percentage |\n")
        f.write("|----------|-------------|----------------|------------|\n")
        for category, stats in category_stats.items():
            f.write(
                f"| {category} | {stats['met']} | {stats['total']} | {stats['percentage']}% |\n"
            )
        f.write("\n")

        # Detailed criteria breakdown
        f.write("## Detailed Criteria Breakdown\n\n")

        # Create non-overlapping criteria lists, only including criteria that exist in assessment
        essential_criteria = [
            crit
            for crit in criteria_categories.get("Essential", [])
            if crit in assessment
        ]
        professional_criteria = [
            crit
            for crit in criteria_categories.get("Professional", [])
            if crit not in essential_criteria and crit in assessment
        ]
        elite_criteria = [
            crit
            for crit in criteria_categories.get("Elite", [])
            if crit not in essential_criteria
            and crit not in professional_criteria
            and crit in assessment
        ]

        # Use the filtered lists for each category
        category_filtered_criteria = {
            "Essential": essential_criteria,
            "Professional": professional_criteria,
            "Elite": elite_criteria,
        }

        for category, criteria_list in category_filtered_criteria.items():
            if not criteria_list:
                continue

            f.write(f"### {category} Criteria\n\n")
            f.write("| Category | Criterion | Status | Explanation |\n")
            f.write("|------------|------------|----------|------------------------|\n")

            for criterion in criteria_list:
                # Find which category this criterion belongs to
                criterion_category = None
                for cat, criteria in category_criteria.items():
                    if criterion in criteria:
                        criterion_category = cat
                        break

                status = "✅" if assessment[criterion].get("score", 0) == 1 else "❌"
                explanation = assessment[criterion].get(
                    "explanation", "No explanation provided"
                )
                f.write(
                    f"| {criterion_category} | {criteria_names[criterion]} | {status} | {explanation} |\n"
                )

            f.write("\n")

    print(f"Report generated successfully at {output_file}")
