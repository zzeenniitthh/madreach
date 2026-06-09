import {
	AbsoluteFill,
	interpolate,
	spring,
	useCurrentFrame,
	useVideoConfig,
} from 'remotion';

export const TitleScene: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	// Big springy entrance for the headline.
	const titleSpring = spring({
		fps,
		frame,
		config: {damping: 12, stiffness: 90, mass: 0.8},
	});
	const titleY = interpolate(titleSpring, [0, 1], [80, 0]);
	const titleOpacity = interpolate(frame, [0, 15], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	// Subtitle slides in slightly delayed.
	const subSpring = spring({
		fps,
		frame: frame - 10,
		config: {damping: 14, stiffness: 80},
	});
	const subY = interpolate(subSpring, [0, 1], [40, 0]);
	const subOpacity = interpolate(frame, [10, 30], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	// Underline draws in.
	const underlineWidth = interpolate(frame, [20, 50], [0, 600], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	return (
		<AbsoluteFill
			style={{
				justifyContent: 'center',
				alignItems: 'center',
				textAlign: 'center',
			}}
		>
			<div
				style={{
					color: '#60a5fa',
					fontSize: 36,
					fontWeight: 600,
					letterSpacing: 8,
					textTransform: 'uppercase',
					opacity: subOpacity,
					transform: `translateY(${subY}px)`,
					marginBottom: 24,
				}}
			>
				Annual Report
			</div>
			<h1
				style={{
					color: 'white',
					fontSize: 130,
					fontWeight: 900,
					margin: 0,
					letterSpacing: -2,
					opacity: titleOpacity,
					transform: `translateY(${titleY}px)`,
					lineHeight: 1.05,
				}}
			>
				GLOBAL AI ADOPTION
			</h1>
			<div
				style={{
					height: 6,
					width: underlineWidth,
					background: 'linear-gradient(90deg, #60a5fa, #a855f7)',
					marginTop: 24,
					borderRadius: 3,
				}}
			/>
			<div
				style={{
					color: 'white',
					fontSize: 110,
					fontWeight: 900,
					marginTop: 18,
					letterSpacing: 4,
					opacity: interpolate(frame, [30, 55], [0, 1], {
						extrapolateLeft: 'clamp',
						extrapolateRight: 'clamp',
					}),
					background: 'linear-gradient(90deg, #60a5fa, #a855f7)',
					WebkitBackgroundClip: 'text',
					WebkitTextFillColor: 'transparent',
				}}
			>
				2025
			</div>
		</AbsoluteFill>
	);
};
