# Anomaly thresholds for regression detection.
# Edit these values to adjust sensitivity.

# WORD_COUNT_RATIO_MIN removed -- low wcr is noise on chrome-heavy sources
# where nav, sidebars, and CMS chrome inflate the raw source word count.
# Kept here as a comment to explain its absence. See decisions.md.
# WORD_COUNT_RATIO_MIN = 0.30

WORD_COUNT_RATIO_MAX = 1.5
# Output larger than 1.5x source word count signals boilerplate or metadata
# leakage into the pipeline output. Catches cases where extraction pulls in
# more content than the raw source contained (e.g. plos-one-open-access).

AVG_PARAGRAPH_WORDS_MIN = 8.0
PLACEHOLDER_DENSITY_MAX = 0.20
LINK_TO_PROSE_RATIO_MAX = 0.50
