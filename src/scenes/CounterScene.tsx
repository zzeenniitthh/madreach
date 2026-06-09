import {
	AbsoluteFill,
	interpolate,
	spring,
	useCurrentFrame,
	useVideoConfig,
} from 'remotion';

const TARGET = 78;

export const CounterScene: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	// Rapid count up, then hold.
	const countProgress = interpolate(frame, [5, 45], [0, TARGET], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});
	const count = Math.min(TARGET, Math.round(countProgress));

	// Pop animation when the counter lands on the target.
	const landSpring = spring({
		fps,
		frame: frame - 45,
		config: {damping: 6, stiffness: 180, mass: 0.6},
	});
	const pop = 1 + landSpring * 0.08 - landSpring * landSpring * 0.04;

	const labelOpacity = interpolate(frame, [40, 60], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	// Circular progress ring follows the counter.
	const ringProgress = countProgress / 100;
	const radius = 280;
	const circumference = 2 * Math.PI * radius;
	const ringOffset = circumference * (1 - ringProgress);

	return (
		<AbsoluteFill
			style={{
				justifyContent: 'center',
				alignItems: 'center',
				flexDirection: 'column',
			}}
		>
			<div
				style={{
					position: 'relative',
					width: 640,
					height: 640,
					display: 'flex',
					justifyContent: 'center',
					alignItems: 'center',
				}}
			>
				<svg
					width={640}
					height={640}
					style={{position: 'absolute', transform: 'rotate(-90deg)'}}
				>
					<circle
						cx={320}
						cy={320}
						r={radius}
						stroke="rgba(148, 163, 184, 0.2)"
						strokeWidth={20}
						fill="none"
					/>
					<circle
						cx={320}
						cy={320}
						r={radius}
						stroke="url(#ringGrad)"
						strokeWidth={20}
						fill="none"
						strokeLinecap="round"
						strokeDasharray={circumference}
						strokeDashoffset={ringOffset}
					/>
					<defs>
						<linearGradient id="ringGrad" x1="0" y1="0" x2="1" y2="1">
							<stop offset="0%" stopColor="#60a5fa" />
							<stop offset="100%" stopColor="#a855f7" />
						</linearGradient>
					</defs>
				</svg>
				<div
					style={{
						display: 'flex',
						alignItems: 'baseline',
						transform: `scale(${pop})`,
					}}
				>
					<div
						style={{
							color: 'white',
							fontSize: 260,
							fontWeight: 900,
							lineHeight: 1,
							fontVariantNumeric: 'tabular-nums',
						}}
					>
						{count}
					</div>
					<div
						style={{
							color: '#a855f7',
							fontSize: 120,
							fontWeight: 900,
							marginLeft: 8,
						}}
					>
						%
					</div>
				</div>
			</div>
			<div
				style={{
					color: 'white',
					fontSize: 48,
					fontWeight: 700,
					marginTop: 32,
					opacity: labelOpacity,
					textAlign: 'center',
				}}
			>
				of companies report using AI
			</div>
		</AbsoluteFill>
	);
};
