// Method created by Claude
export function getTextColorForHexBg(hex: string | undefined) {
	if (!hex) {
		return "";
	}

	// Strip leading # if present
	hex = hex.replace(/^#/, "");

	// Expand shorthand (e.g. "03F") to full form ("0033FF")
	if (hex.length === 3) {
		hex = hex
			.split("")
			.map((c) => c + c)
			.join("");
	}

	if (!/^[0-9A-Fa-f]{6}$/.test(hex)) {
		throw new Error(`Invalid hex color: "${hex}"`);
	}

	const r = parseInt(hex.slice(0, 2), 16) / 255;
	const g = parseInt(hex.slice(2, 4), 16) / 255;
	const b = parseInt(hex.slice(4, 6), 16) / 255;

	// Convert sRGB to linear RGB (gamma correction)
	const linearize = (c: number) => (c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4));

	const [rl, gl, bl] = [r, g, b].map(linearize);

	// Relative luminance (WCAG formula)
	const luminance = 0.2126 * rl + 0.7152 * gl + 0.0722 * bl;

	// Threshold ~0.179 gives a good black/white split against WCAG contrast ratios
	return luminance > 0.179 ? "black" : "white";
}
