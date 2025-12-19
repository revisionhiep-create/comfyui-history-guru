/**
 * Preset trigger words for Standard Trigger Words Loader
 * Embedded directly in JavaScript for easy access
 */

export const TRIGGER_WORD_PRESETS = {
    "Quality": [
        "masterpiece",
        "best quality",
        "very aesthetic",
        "absurdres",
        "high quality",
        "ultra high definition",
        "extremely high detail",
        "newest",
        "year 2024",
        "year 2025",
        "highres",
        "8K",
        "HDR",
    ],
    "Lighting": [
        "volumetric lighting",
        "ambient occlusion",
        "dramatic lighting",
        "cinematic lighting",
        "rim light",
        "soft lighting",
        "studio lighting",
        "golden hour lighting",
        "natural lighting",
        "sunlight",
        "backlighting",
        "sharp focus",
        "glowing",
        "luminescent background",
    ],
    "Composition": [
        "dynamic angle",
        "dynamic pose",
        "low-angle shot",
        "low angle",
        "looking at viewer",
        "from above",
        "from below",
        "upper body focus",
        "full body",
        "portrait",
        "close-up shot",
        "mid shot",
        "cowboy shot",
        "wide angle",
        "cinematic field of view",
        "perfect composition",
        "rule of thirds",
    ],
    "Style": [
        "anime illustration",
        "semi-realistic anime illustration",
        "digital painting",
        "cel shading",
        "clean linework",
        "manga style lineart",
        "detailed",
        "highly detailed",
        "intricate details",
        "painterly",
    ],
    "Detail": [
        "detailed eyes",
        "beautiful eye details",
        "detailed skin features",
        "detailed face features",
        "detailed hair features",
        "expressive eyes",
        "intricate iris",
        "detailed clothing",
        "detailed background",
        "fine texture details",
    ],
    "Aesthetic": [
        "beautiful",
        "amazing",
        "stunning",
        "gorgeous",
        "perfect",
        "flawless",
        "eye-catching",
        "stylish",
        "elegant",
        "aesthetic",
    ],
    "Motion": [
        "motion blur",
        "motion lines",
        "action pose",
        "dynamic action",
        "movement",
        "speed lines",
        "flowing",
        "fluid motion",
    ],
};

// Combine all categories
TRIGGER_WORD_PRESETS["All"] = Object.values(TRIGGER_WORD_PRESETS).flat();

export function getPresetTags(category, defaultActive = true, defaultStrength = 1.0) {
    const words = TRIGGER_WORD_PRESETS[category] || [];
    return words.map(text => ({
        text: text,
        active: defaultActive,
        strength: defaultStrength
    }));
}
