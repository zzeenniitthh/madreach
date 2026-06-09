import {
	AbsoluteFill,
	interpolate,
	spring,
	useCurrentFrame,
	useVideoConfig,
} from 'remotion';

export const ClosingScene: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	const headlineSpring = spring({
		fps,
		frame,
		config: {damping: 14, stiffness: 90},
	});
	const headlineY = interpolate(headlineSpring, [0, 1], [40, 0]);
	const headlineOpacity = interpolate(frame, [0, 18], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	const subOpacity = interpolate(frame, [15, 35], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	const lineWidth = interpolate(frame, [10, 40], [0, 800], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	return (
		<AbsoluteFill
			style={{
				justifyContent: 'center',
				alignItems: 'center',
				textAlign: 'center',
				flexDirection: 'column',
			}}
		>
			<div
				style={{
					height: 4,
					width: lineWidth,
					background: 'linear-gradient(90deg, transparent, #60a5fa, #a855f7, transparent)',
					marginBottom: 40,
				}}
			/>
			<h1
				style={{
					color: 'white',
					fontSize: 110,
					fontWeight: 900,
					margin: 0,
					letterSpacing: -2,
					opacity: headlineOpacity,
					transform: `translateY(${headlineY}px)`,
					lineHeight: 1.1,
				}}
			>
				The Future is{' '}
				<span
					style={{
						background: 'linear-gradient(90deg, #60a5fa, #a855f7)',
						WebkitBackgroundClip: 'text',
						WebkitTextFillColor: 'transparent',
					}}
				>
					Intelligent
				</span>
			</h1>
			<div
				style={{
					color: '#94a3b8',
					fontSize: 36,
					marginTop: 32,
					letterSpacing: 4,
					textTransform: 'uppercase',
					opacity: subOpacity,
				}}
			>
				Source: Global AI Adoption Index · 2025
			</div>
			<div
				style={{
					height: 4,
					width: lineWidth,
					background: 'linear-gradient(90deg, transparent, #a855f7, #60a5fa, transparent)',
					marginTop: 40,
				}}
			/>
		</AbsoluteFill>
	);
};
