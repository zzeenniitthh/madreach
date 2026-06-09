import React from 'react';
import {
	AbsoluteFill,
	interpolate,
	random,
	spring,
	useCurrentFrame,
	useVideoConfig,
} from 'remotion';
import {loadFont as loadInter} from '@remotion/google-fonts/Inter';
import {loadFont as loadMono} from '@remotion/google-fonts/JetBrainsMono';

const {fontFamily: INTER} = loadInter('normal', {weights: ['400', '800']});
const {fontFamily: MONO} = loadMono('normal', {weights: ['400', '500']});

// --- Palette ---------------------------------------------------------------
const BG = '#0A0A0A'; // near-black background
const WHITE = '#E5E5E5'; // default text
const GREEN = '#39FF14'; // accent / prompt / command / cursor
const GRAY = '#8A8A8A'; // dimmed subtext

// --- Copy ------------------------------------------------------------------
const CMD = 'request-access';
const URL = 'remoroo.com/autonomous-data';
const TAGLINE = "Bring your codebase and a metric. We'll move it.";

// --- Timeline (30fps, 120 frames = 4.0s) -----------------------------------
const WORDMARK_END = 15; // 0.0–0.5s : wordmark fades + scales in
const PROMPT_START = 15; // 0.5s     : green ❯ appears
const PROMPT_END = 18;
const TYPE_START = 18;
const TYPE_END = 48; // 1.6s     : "request-access" finished typing
const URL_START = 48; // 1.6–2.0s : url fades in
const URL_END = 60;
const TAGLINE_START = 60; // 2.0–2.4s : tagline fades in
const TAGLINE_END = 72;
const HOLD_START = 72; // 2.4–4.0s : everything holds, glow breathes

// Average frames per character across the typing window, with light human
// jitter so the cadence doesn't feel mechanical (~1 char / ~2 frames here).
const AVG_PER_CHAR = (TYPE_END - TYPE_START) / CMD.length;

const charsTypedAt = (frame: number): number => {
	if (frame <= TYPE_START) return 0;
	if (frame >= TYPE_END) return CMD.length;
	const elapsed = frame - TYPE_START;
	let acc = 0;
	for (let i = 0; i < CMD.length; i++) {
		const jitter = (random(`remoroo-type-${i}`) - 0.5) * 0.9;
		acc += Math.max(0.5, AVG_PER_CHAR + jitter);
		if (acc > elapsed) return i;
	}
	return CMD.length;
};

const Cursor: React.FC<{opacity: number}> = ({opacity}) => (
	<span
		style={{
			display: 'inline-block',
			width: '0.55em',
			height: '1.05em',
			background: GREEN,
			marginLeft: 6,
			borderRadius: 1,
			transform: 'translateY(3px)',
			opacity,
		}}
	/>
);

export const RemorooEndCard: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	// Wordmark: gentle spring scale 0.94 -> 1.0, opacity 0 -> 1.
	const wordmarkSpring = spring({
		frame,
		fps,
		config: {damping: 200},
		durationInFrames: WORDMARK_END,
	});
	const wordmarkScale = interpolate(wordmarkSpring, [0, 1], [0.94, 1]);
	const wordmarkOpacity = interpolate(frame, [0, WORDMARK_END], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	// CTA prompt + typed command.
	const promptOpacity = interpolate(frame, [PROMPT_START, PROMPT_END], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});
	const charsTyped = charsTypedAt(frame);
	const isTyping = frame >= TYPE_START && frame < TYPE_END;

	// Cursor: solid while typing, soft sinusoidal blink (~0.5s) otherwise.
	const blink = (Math.sin((frame / 15) * Math.PI) + 1) / 2; // 0..1, ~30f cycle
	const blinkSoft = interpolate(blink, [0, 1], [0.15, 1]);
	const cursorOpacity =
		frame < PROMPT_START ? 0 : isTyping ? 1 : blinkSoft;

	// URL + tagline fades.
	const urlOpacity = interpolate(frame, [URL_START, URL_END], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});
	const taglineOpacity = interpolate(
		frame,
		[TAGLINE_START, TAGLINE_END],
		[0, 1],
		{extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
	);

	// Subtle green radial glow behind the wordmark: ramps in with the wordmark,
	// then breathes almost imperceptibly through the hold.
	const glowBase = interpolate(frame, [0, WORDMARK_END], [0, 0.08], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});
	const pulse =
		frame >= HOLD_START
			? Math.sin(((frame - HOLD_START) / 60) * Math.PI * 2) * 0.04
			: 0;
	const glowOpacity = Math.max(0, glowBase + pulse);

	return (
		<AbsoluteFill style={{backgroundColor: BG}}>
			<AbsoluteFill
				style={{
					display: 'flex',
					flexDirection: 'column',
					alignItems: 'center',
					justifyContent: 'center',
					gap: 64,
					paddingBottom: 40,
				}}
			>
				{/* Wordmark with soft green glow behind */}
				<div
					style={{
						position: 'relative',
						transform: `scale(${wordmarkScale})`,
						opacity: wordmarkOpacity,
					}}
				>
					<div
						style={{
							position: 'absolute',
							top: '50%',
							left: '50%',
							width: 900,
							height: 380,
							transform: 'translate(-50%, -50%)',
							background: `radial-gradient(closest-side, ${GREEN}, transparent 70%)`,
							opacity: glowOpacity,
							filter: 'blur(50px)',
							pointerEvents: 'none',
						}}
					/>
					<div
						style={{
							position: 'relative',
							color: WHITE,
							fontFamily: INTER,
							fontWeight: 800,
							textTransform: 'uppercase',
							letterSpacing: '0.15em',
							// pad right so wide tracking stays optically centered
							paddingLeft: '0.15em',
							fontSize: 92,
							lineHeight: 1,
						}}
					>
						REMOROO
					</div>
				</div>

				{/* CTA command line */}
				<div
					style={{
						fontFamily: MONO,
						fontWeight: 500,
						fontSize: 34,
						lineHeight: 1.2,
						whiteSpace: 'pre',
						display: 'flex',
						alignItems: 'center',
					}}
				>
					<span style={{color: GREEN, opacity: promptOpacity}}>{'❯ '}</span>
					<span style={{color: GREEN}}>{CMD.slice(0, charsTyped)}</span>
					<Cursor opacity={cursorOpacity} />
				</div>

				{/* URL */}
				<div
					style={{
						fontFamily: MONO,
						fontWeight: 400,
						fontSize: 24,
						color: GRAY,
						opacity: urlOpacity,
						letterSpacing: '0.02em',
						marginTop: -28,
					}}
				>
					{URL}
				</div>
			</AbsoluteFill>

			{/* Tagline pinned near the bottom */}
			<div
				style={{
					position: 'absolute',
					bottom: 80,
					left: 0,
					right: 0,
					textAlign: 'center',
					opacity: taglineOpacity,
					color: GRAY,
					fontFamily: INTER,
					fontWeight: 400,
					fontSize: 20,
					letterSpacing: '0.04em',
				}}
			>
				{TAGLINE}
			</div>
		</AbsoluteFill>
	);
};
