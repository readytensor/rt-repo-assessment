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
        assessment_file: Path to the assessment.json file
        output_file: Path where to save the Markdown report
        criteria_categories: Dictionary mapping category names to lists of criteria IDs
    """

    total_criteria = len(assessment)
    met_criteria = sum(1 for score in assessment.values() if score.get("score", 0) == 1)

    # Calculate statistics by category
    category_stats = {}
    for category, criteria_list in criteria_categories.items():
        total_in_category = len(criteria_list)
        met_in_category = sum(
            1
            for crit in criteria_list
            if crit in assessment and assessment[crit].get("score", 0) == 1
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

        # Create non-overlapping criteria lists
        essential_criteria = criteria_categories.get("Essential", [])
        professional_criteria = [
            crit
            for crit in criteria_categories.get("Professional", [])
            if crit not in essential_criteria
        ]
        elite_criteria = [
            crit
            for crit in criteria_categories.get("Elite", [])
            if crit not in essential_criteria and crit not in professional_criteria
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

                if criterion in assessment:
                    status = (
                        "✅ Met"
                        if assessment[criterion].get("score", 0) == 1
                        else "❌ Not Met"
                    )
                    explanation = assessment[criterion].get(
                        "explanation", "No explanation provided"
                    )
                    f.write(
                        f"| {criterion_category} | {criteria_names[criterion]} | {status} | {explanation} |\n"
                    )
                else:
                    f.write(
                        f"| {criterion_category} | {criteria_names[criterion]} | ❓ Not Evaluated | - |\n"
                    )

            f.write("\n")

    print(f"Report generated successfully at {output_file}")
