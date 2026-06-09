import React from 'react';
import {
	AbsoluteFill,
	interpolate,
	random,
	spring,
	useCurrentFrame,
	useVideoConfig,
} from 'remotion';

const BG = '#0A0A0A';
const WHITE = '#E5E5E5';
const GREEN = '#39FF14';
const GRAY = '#8A8A8A';

const FONT_MONO =
	'"JetBrains Mono", "Fira Code", "SF Mono", Menlo, Consolas, monospace';
const FONT_SANS =
	'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif';

// 30 fps, 120-frame end-card
const LOGO_END = 15; // 0.5s
const PROMPT_END = 18; // green ❯ appears
const TYPE_START = 18;
const TYPE_END = 48; // 1.6s
const URL_START = 48;
const URL_END = 60; // 2.0s
const TAGLINE_START = 60;
const TAGLINE_END = 72; // 2.4s
const HOLD_START = 72;

const CMD = 'request-access';
const TOTAL_CHARS = CMD.length;

const TYPE_AVG = (TYPE_END - TYPE_START) / TOTAL_CHARS; // ~2.14 frames per char

const getCharsTyped = (frame: number): number => {
	if (frame <= TYPE_START) return 0;
	if (frame >= TYPE_END) return TOTAL_CHARS;
	const elapsed = frame - TYPE_START;
	let acc = 0;
	for (let i = 0; i < TOTAL_CHARS; i++) {
		const jitter = (random(`endcard-type-${i}`) - 0.5) * 0.9;
		acc += Math.max(0.5, TYPE_AVG + jitter);
		if (acc > elapsed) return i;
	}
	return TOTAL_CHARS;
};

const Cursor: React.FC<{visible: boolean}> = ({visible}) => (
	<span
		style={{
			display: 'inline-block',
			width: '0.55em',
			height: '1.05em',
			background: GREEN,
			verticalAlign: 'text-bottom',
			marginLeft: 4,
			opacity: visible ? 1 : 0,
			transform: 'translateY(2px)',
		}}
	/>
);

export const EndCard: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	// Logo entrance
	const logoSpring = spring({
		frame,
		fps,
		config: {damping: 200},
		durationInFrames: 15,
	});
	const logoScale = interpolate(logoSpring, [0, 1], [0.94, 1]);
	const logoOpacity = interpolate(frame, [0, LOGO_END], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	// Command line
	const promptOpacity = interpolate(
		frame,
		[LOGO_END, PROMPT_END],
		[0, 1],
		{extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
	);
	const charsTyped = getCharsTyped(frame);
	const isActivelyTyping = frame >= TYPE_START && frame < TYPE_END;
	const blinkOn = frame % 30 < 15;
	const cursorVisible =
		frame >= PROMPT_END && (isActivelyTyping ? true : blinkOn);

	// URL
	const urlOpacity = interpolate(frame, [URL_START, URL_END], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	// Tagline
	const taglineOpacity = interpolate(
		frame,
		[TAGLINE_START, TAGLINE_END],
		[0, 1],
		{extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
	);

	// Subtle behind-logo glow that ramps in with the logo and breathes during hold
	const glowBase = interpolate(frame, [0, LOGO_END], [0, 0.09], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});
	const pulseElapsed = Math.max(0, frame - HOLD_START);
	const pulseAdd =
		frame >= HOLD_START
			? Math.sin((pulseElapsed / 75) * Math.PI * 2) * 0.05
			: 0;
	const glowOpacity = Math.max(0, glowBase + pulseAdd);

	return (
		<AbsoluteFill style={{background: BG, fontFamily: FONT_MONO}}>
			<AbsoluteFill
				style={{
					display: 'flex',
					flexDirection: 'column',
					alignItems: 'center',
					justifyContent: 'center',
					gap: 56,
					paddingBottom: 60,
				}}
			>
				{/* Logo with soft green glow behind */}
				<div
					style={{
						position: 'relative',
						transform: `scale(${logoScale})`,
						opacity: logoOpacity,
					}}
				>
					<div
						style={{
							position: 'absolute',
							top: '50%',
							left: '50%',
							width: 720,
							height: 360,
							transform: 'translate(-50%, -50%)',
							background: `radial-gradient(closest-side, ${GREEN}, transparent 70%)`,
							opacity: glowOpacity,
							filter: 'blur(40px)',
							pointerEvents: 'none',
						}}
					/>
					<div
						style={{
							display: 'flex',
							alignItems: 'center',
							gap: 30,
							position: 'relative',
						}}
					>
						<svg width="58" height="70" viewBox="0 0 58 70">
							<polygon points="6,4 6,66 54,35" fill={GREEN} />
						</svg>
						<div
							style={{
								color: WHITE,
								fontFamily: FONT_SANS,
								fontWeight: 800,
								letterSpacing: 11,
								fontSize: 56,
							}}
						>
							REMOROO
						</div>
					</div>
				</div>

				{/* Command-prompt CTA */}
				<div
					style={{
						fontSize: 32,
						lineHeight: 1.2,
						whiteSpace: 'pre',
						display: 'flex',
						alignItems: 'baseline',
					}}
				>
					<span style={{color: GREEN, opacity: promptOpacity}}>{'❯ '}</span>
					<span style={{color: GREEN}}>{CMD.slice(0, charsTyped)}</span>
					<Cursor visible={cursorVisible} />
				</div>

				{/* URL */}
				<div
					style={{
						fontSize: 22,
						color: GRAY,
						opacity: urlOpacity,
						letterSpacing: 0.5,
						marginTop: -24,
					}}
				>
					remoroo.com/access
				</div>
			</AbsoluteFill>

			{/* Tagline pinned near the bottom */}
			<div
				style={{
					position: 'absolute',
					bottom: 72,
					left: 0,
					right: 0,
					textAlign: 'center',
					opacity: taglineOpacity,
					color: GRAY,
					fontFamily: FONT_SANS,
					fontSize: 18,
					letterSpacing: 0.6,
				}}
			>
				Bring your codebase and a metric. We&apos;ll move it.
			</div>
		</AbsoluteFill>
	);
};
