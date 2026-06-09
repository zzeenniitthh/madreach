import React from 'react';
import {
	AbsoluteFill,
	Easing,
	interpolate,
	spring,
	useCurrentFrame,
	useVideoConfig,
} from 'remotion';
import {loadFont as loadInter} from '@remotion/google-fonts/Inter';
import {loadFont as loadMono} from '@remotion/google-fonts/JetBrainsMono';

const {fontFamily: INTER} = loadInter('normal', {
	weights: ['300', '500'],
});
const {fontFamily: MONO} = loadMono('normal', {weights: ['400']});

// --- Palette ---------------------------------------------------------------
const GREEN = '#39FF14'; // lime accent — used sparingly
const OFFWHITE = '#F5F5F5';
const MUTED = '#777777';
const GLASS = '#1A1A1A'; // button fill

// --- Timeline (30fps, 120 frames = 4.0s) -----------------------------------
const LINE1_IN = 0; // 0.0–0.6s : bg + glow + tagline line 1
const LINE2_IN = 18; // 0.6–1.0s : tagline line 2 (green)
const BUTTON_IN = 30; // 1.0–1.7s : button springs in, border illuminates
const SHEEN_START = 51; // 1.7–2.1s : light sweep across glass
const SHEEN_END = 63;
const URL_IN = 63; // 2.1–2.5s : url fades in
const HOLD_START = 75; // 2.5–4.0s : breathing glow + arrow nudge

// Reusable "fade + rise" entrance driven by a soft spring.
const useRiseIn = (start: number, fps: number, frame: number, rise = 12) => {
	const s = spring({
		frame: frame - start,
		fps,
		config: {damping: 200, mass: 0.8},
		durationInFrames: 18,
	});
	return {
		opacity: s,
		translateY: interpolate(s, [0, 1], [rise, 0]),
	};
};

export const RequestAccessCard: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	// Tagline.
	const line1 = useRiseIn(LINE1_IN, fps, frame);

	// Button entrance: soft spring, scale 0.92 -> 1.0.
	const buttonSpring = spring({
		frame: frame - BUTTON_IN,
		fps,
		config: {damping: 200, mass: 1},
		durationInFrames: 21,
	});
	const buttonScale = interpolate(buttonSpring, [0, 1], [0.92, 1]);
	const buttonOpacity = buttonSpring;

	// Border + glow illuminate as the button lands.
	const illuminate = interpolate(
		frame,
		[BUTTON_IN, BUTTON_IN + 18],
		[0, 1],
		{extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
	);

	// Light sheen sweep: a skewed highlight travels left -> right once.
	const sheen = interpolate(frame, [SHEEN_START, SHEEN_END], [-140, 240], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
		easing: Easing.inOut(Easing.cubic),
	});
	const sheenVisible = frame >= SHEEN_START && frame <= SHEEN_END + 2;

	// URL fade.
	const urlOpacity = interpolate(frame, [URL_IN, URL_IN + 12], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	// Hold: slow breathing of the glow (~2s cycle) + gentle arrow nudge.
	const breathe =
		(Math.sin(((frame - HOLD_START) / 60) * Math.PI * 2 - Math.PI / 2) + 1) /
		2; // 0..1, 60-frame cycle
	const glowBreath = frame >= HOLD_START ? interpolate(breathe, [0, 1], [0, 1]) : 0;
	// Base glow blooms with entrance, then breathes during hold.
	const glowStrength = illuminate * (0.55 + 0.45 * glowBreath);

	const arrowNudge =
		frame >= HOLD_START
			? Math.sin(((frame - HOLD_START) / 45) * Math.PI * 2) * 2.5 + 2.5
			: 0;

	// Faint, slow-drifting green glow behind the button center.
	const ambientGlow = interpolate(frame, [0, 18], [0, 0.5], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});
	const driftX = Math.sin((frame / 90) * Math.PI * 2) * 26;
	const driftY = Math.cos((frame / 110) * Math.PI * 2) * 18;

	return (
		<AbsoluteFill
			style={{
				// Depth: radial gradient from #141414 center to #0A0A0A edges.
				background:
					'radial-gradient(ellipse 80% 80% at 50% 50%, #141414 0%, #0A0A0A 100%)',
			}}
		>
			{/* Fine deterministic grain to dither the gradient and kill 8-bit
			    banding. SVG turbulence is render-stable (no Math.random). */}
			<svg
				style={{
					position: 'absolute',
					inset: 0,
					width: '100%',
					height: '100%',
					opacity: 0.045,
					mixBlendMode: 'overlay',
					pointerEvents: 'none',
				}}
			>
				<filter id="ra-grain">
					<feTurbulence
						type="fractalNoise"
						baseFrequency="0.9"
						numOctaves={2}
						stitchTiles="stitch"
					/>
					<feColorMatrix type="saturate" values="0" />
				</filter>
				<rect width="100%" height="100%" filter="url(#ra-grain)" />
			</svg>

			{/* Ambient drifting green glow behind the focal point */}
			<AbsoluteFill
				style={{
					justifyContent: 'center',
					alignItems: 'center',
				}}
			>
				<div
					style={{
						position: 'absolute',
						width: 400,
						height: 150,
						transform: `translate(${driftX}px, ${driftY}px)`,
						background: `radial-gradient(closest-side, ${GREEN}, transparent 55%)`,
						opacity: 0.06 * ambientGlow + 0.04 * glowBreath * illuminate,
						filter: 'blur(28px)',
						pointerEvents: 'none',
					}}
				/>
			</AbsoluteFill>

			{/* Centered stack: tagline / button / url */}
			<AbsoluteFill
				style={{
					display: 'flex',
					flexDirection: 'column',
					alignItems: 'center',
					justifyContent: 'center',
					gap: 64,
				}}
			>
				{/* Tagline */}
				<div
					style={{
						textAlign: 'center',
						fontFamily: INTER,
						fontWeight: 300,
						fontSize: 40,
						lineHeight: 1.32,
						letterSpacing: '0.005em',
						color: OFFWHITE,
						opacity: line1.opacity,
						transform: `translateY(${line1.translateY}px)`,
					}}
				>
					Get it today
				</div>

				{/* Hero CTA button */}
				<div
					style={{
						transform: `scale(${buttonScale})`,
						opacity: buttonOpacity,
						position: 'relative',
					}}
				>
					{/* Soft outer glow bloom */}
					<div
						style={{
							position: 'absolute',
							inset: -2,
							borderRadius: 16,
							boxShadow: `0 0 ${20 + 26 * glowBreath}px ${
								4 + 6 * glowBreath
							}px rgba(57, 255, 20, ${0.18 + 0.14 * glowStrength})`,
							pointerEvents: 'none',
						}}
					/>
					{/* The button itself */}
					<div
						style={{
							position: 'relative',
							width: 380,
							height: 84,
							borderRadius: 14,
							background: GLASS,
							border: `1.5px solid rgba(57, 255, 20, ${
								0.25 + 0.75 * illuminate
							})`,
							display: 'flex',
							alignItems: 'center',
							justifyContent: 'center',
							gap: 12,
							overflow: 'hidden',
							boxShadow:
								'inset 0 1px 0 rgba(255,255,255,0.04), 0 8px 30px rgba(0,0,0,0.5)',
						}}
					>
						{/* Light sheen sweeping across the glass */}
						{sheenVisible && (
							<div
								style={{
									position: 'absolute',
									top: 0,
									left: 0,
									width: '60%',
									height: '100%',
									transform: `translateX(${sheen}%) skewX(-18deg)`,
									background:
										'linear-gradient(100deg, transparent, rgba(57,255,20,0.18), rgba(245,245,245,0.10), transparent)',
									pointerEvents: 'none',
								}}
							/>
						)}
						<span
							style={{
								fontFamily: INTER,
								fontWeight: 500,
								fontSize: 27,
								color: OFFWHITE,
								letterSpacing: '0.01em',
							}}
						>
							Request access
						</span>
						<span
							style={{
								fontFamily: INTER,
								fontWeight: 500,
								fontSize: 27,
								color: GREEN,
								transform: `translateX(${arrowNudge}px)`,
								display: 'inline-block',
							}}
						>
							→
						</span>
					</div>
				</div>

				{/* URL */}
				<div
					style={{
						fontFamily: MONO,
						fontWeight: 400,
						fontSize: 22,
						color: MUTED,
						opacity: urlOpacity,
						letterSpacing: '0.02em',
					}}
				>
					remoroo.com/autonomous-data
				</div>
			</AbsoluteFill>
		</AbsoluteFill>
	);
};
