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
const WIN_BG = '#111111';
const WHITE = '#E5E5E5';
const GREEN = '#39FF14';
const GRAY = '#8A8A8A';
const BORDER = '#1F1F1F';
const DOT = '#333333';

const FONT_MONO =
	'"JetBrains Mono", "Fira Code", "SF Mono", Menlo, Consolas, monospace';
const FONT_SANS =
	'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif';

const TYPE_START = 12;
const TYPE_END = 108;
const ENTER_START = 117;
const HOLD_START = 123;

type Token = {text: string; color: string};

const LINES: Token[][] = [
	[
		{text: 'remoroo', color: GREEN},
		{text: ' robot run \\', color: WHITE},
	],
	[
		{text: '  ', color: WHITE},
		{text: '--goal', color: GRAY},
		{text: ' ', color: WHITE},
		{text: '"clear the table into the black box"', color: WHITE},
		{text: ' \\', color: WHITE},
	],
	[
		{text: '  ', color: WHITE},
		{text: '--target', color: GRAY},
		{text: ' ', color: WHITE},
		{text: '"100% success or 100 trials"', color: WHITE},
	],
];

const LINE_CHARS = LINES.map((line) =>
	line.reduce((sum, tok) => sum + tok.text.length, 0),
);
const LINE_STARTS = LINE_CHARS.map((_, i) =>
	LINE_CHARS.slice(0, i).reduce((s, n) => s + n, 0),
);
const TOTAL_CHARS = LINE_CHARS.reduce((s, n) => s + n, 0);

// Frames per char, with deterministic jitter, calibrated so all chars finish
// before TYPE_END.
const TYPE_FRAMES = TYPE_END - TYPE_START;
const AVG_CHAR_COST = TYPE_FRAMES / TOTAL_CHARS;

const getCharsTyped = (frame: number): number => {
	if (frame <= TYPE_START) return 0;
	if (frame >= TYPE_END) return TOTAL_CHARS;
	const elapsed = frame - TYPE_START;
	let acc = 0;
	for (let i = 0; i < TOTAL_CHARS; i++) {
		const jitter = (random(`type-${i}`) - 0.5) * 0.5;
		acc += Math.max(0.4, AVG_CHAR_COST + jitter);
		if (acc > elapsed) return i;
	}
	return TOTAL_CHARS;
};

const lineSlice = (lineIdx: number, charsTyped: number): Token[] => {
	let rem = Math.max(0, charsTyped - LINE_STARTS[lineIdx]);
	const out: Token[] = [];
	for (const tok of LINES[lineIdx]) {
		if (rem <= 0) break;
		const take = Math.min(tok.text.length, rem);
		out.push({text: tok.text.slice(0, take), color: tok.color});
		rem -= take;
	}
	return out;
};

const Cursor: React.FC<{visible: boolean}> = ({visible}) => (
	<span
		style={{
			display: 'inline-block',
			width: '0.55em',
			height: '1.1em',
			background: GREEN,
			verticalAlign: 'text-bottom',
			marginLeft: 2,
			opacity: visible ? 1 : 0,
			transform: 'translateY(2px)',
		}}
	/>
);

export const MyComp: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	// Window entrance: spring-driven scale + linear opacity over 0-0.4s
	const windowSpring = spring({
		frame,
		fps,
		config: {damping: 200},
		durationInFrames: 14,
	});
	const windowScale = interpolate(windowSpring, [0, 1], [0.96, 1]);
	const windowOpacity = interpolate(frame, [0, 12], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	const charsTyped = getCharsTyped(frame);

	// A line is visible once typing has reached its start. Line 0 is always visible.
	const visibleLineIndices = LINES.map((_, i) => i).filter(
		(i) => i === 0 || charsTyped >= LINE_STARTS[i],
	);
	const cursorLineIdx =
		visibleLineIndices[visibleLineIndices.length - 1] ?? 0;

	// 0.5s blink cycle = 15 on / 15 off. During active typing, keep cursor solid.
	const blinkOn = frame % 30 < 15;
	const isTyping = frame >= TYPE_START && frame < TYPE_END;
	const cmdCursorVisible = isTyping ? true : blinkOn;
	const showCursorOnCmd = frame < ENTER_START;

	// Enter / init line
	const showInitLine = frame >= ENTER_START;
	const initOpacity = interpolate(
		frame,
		[ENTER_START, ENTER_START + 6],
		[0, 1],
		{extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
	);

	// Subtle underline pulse during hold
	const pulseElapsed = frame - HOLD_START;
	const pulseT = Math.max(0, pulseElapsed) / 60; // period ~2s
	const pulseOpacity =
		pulseElapsed >= 0
			? interpolate(Math.sin(pulseT * Math.PI * 2), [-1, 1], [0.04, 0.18])
			: 0;

	return (
		<AbsoluteFill style={{background: BG, fontFamily: FONT_MONO}}>
			{/* Remoroo logo, top-left of the frame */}
			<div
				style={{
					position: 'absolute',
					top: 56,
					left: 80,
					display: 'flex',
					alignItems: 'center',
					gap: 14,
					opacity: windowOpacity,
				}}
			>
				<svg width="20" height="24" viewBox="0 0 20 24">
					<polygon points="2,2 2,22 19,12" fill={GREEN} />
				</svg>
				<div
					style={{
						color: WHITE,
						fontFamily: FONT_SANS,
						fontWeight: 700,
						letterSpacing: 4,
						fontSize: 17,
					}}
				>
					REMOROO
				</div>
			</div>

			<AbsoluteFill
				style={{
					display: 'flex',
					alignItems: 'center',
					justifyContent: 'center',
				}}
			>
				<div
					style={{
						transform: `scale(${windowScale})`,
						opacity: windowOpacity,
						position: 'relative',
					}}
				>
					{/* Soft green underline pulse beneath the window */}
					<div
						style={{
							position: 'absolute',
							left: '12%',
							right: '12%',
							bottom: -34,
							height: 2,
							background: GREEN,
							opacity: pulseOpacity,
							filter: 'blur(3px)',
							borderRadius: 2,
						}}
					/>
					<div
						style={{
							width: 1100,
							background: WIN_BG,
							borderRadius: 12,
							border: `1px solid ${BORDER}`,
							boxShadow:
								'0 30px 80px rgba(0,0,0,0.55), 0 8px 24px rgba(0,0,0,0.4)',
							overflow: 'hidden',
						}}
					>
						{/* Title bar with muted traffic-light dots */}
						<div
							style={{
								height: 40,
								padding: '0 18px',
								display: 'flex',
								alignItems: 'center',
								gap: 9,
								borderBottom: `1px solid ${BORDER}`,
							}}
						>
							<span
								style={{
									width: 12,
									height: 12,
									borderRadius: '50%',
									background: DOT,
								}}
							/>
							<span
								style={{
									width: 12,
									height: 12,
									borderRadius: '50%',
									background: DOT,
								}}
							/>
							<span
								style={{
									width: 12,
									height: 12,
									borderRadius: '50%',
									background: DOT,
								}}
							/>
						</div>

						{/* Body */}
						<div
							style={{
								padding: '32px 36px 36px',
								color: WHITE,
								fontSize: 22,
								lineHeight: 1.55,
								minHeight: 320,
							}}
						>
							{LINES.map((_, idx) => {
								if (!visibleLineIndices.includes(idx)) return null;
								const tokens = lineSlice(idx, charsTyped);
								const isPromptLine = idx === 0;
								const isCursorHere =
									idx === cursorLineIdx && showCursorOnCmd;
								return (
									<div key={idx} style={{whiteSpace: 'pre'}}>
										{isPromptLine && (
											<span style={{color: GREEN}}>{'❯ '}</span>
										)}
										{tokens.map((tok, i) => (
											<span key={i} style={{color: tok.color}}>
												{tok.text}
											</span>
										))}
										{isCursorHere && (
											<Cursor visible={cmdCursorVisible} />
										)}
									</div>
								);
							})}

							{showInitLine && (
								<div
									style={{
										whiteSpace: 'pre',
										opacity: initOpacity,
										marginTop: 10,
										color: GREEN,
									}}
								>
									<span>{'❯ initializing run...'}</span>
									<Cursor visible={blinkOn} />
								</div>
							)}
						</div>
					</div>
				</div>
			</AbsoluteFill>
		</AbsoluteFill>
	);
};
