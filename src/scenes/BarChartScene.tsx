import {
	AbsoluteFill,
	interpolate,
	spring,
	useCurrentFrame,
	useVideoConfig,
} from 'remotion';

type Bar = {
	industry: string;
	value: number; // percent
	color: string;
};

const BARS: Bar[] = [
	{industry: 'Technology', value: 92, color: '#60a5fa'},
	{industry: 'Finance', value: 81, color: '#a855f7'},
	{industry: 'Healthcare', value: 68, color: '#ec4899'},
	{industry: 'Retail', value: 57, color: '#f59e0b'},
	{industry: 'Manufacturing', value: 44, color: '#10b981'},
];

const CHART_HEIGHT = 560;
const MAX_VALUE = 100;

export const BarChartScene: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	const headerOpacity = interpolate(frame, [0, 18], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	return (
		<AbsoluteFill
			style={{
				padding: '80px 140px',
				flexDirection: 'column',
			}}
		>
			<h2
				style={{
					color: 'white',
					fontSize: 64,
					fontWeight: 800,
					margin: 0,
					opacity: headerOpacity,
				}}
			>
				Adoption Rate by Industry
			</h2>
			<div
				style={{
					color: '#94a3b8',
					fontSize: 28,
					marginTop: 8,
					opacity: headerOpacity,
				}}
			>
				% of organizations using AI in production
			</div>

			<div
				style={{
					flex: 1,
					display: 'flex',
					justifyContent: 'space-around',
					alignItems: 'flex-end',
					marginTop: 60,
					paddingBottom: 80,
					position: 'relative',
				}}
			>
				{/* Y axis gridlines */}
				{[0, 25, 50, 75, 100].map((tick) => {
					const y = CHART_HEIGHT - (tick / MAX_VALUE) * CHART_HEIGHT;
					return (
						<div
							key={tick}
							style={{
								position: 'absolute',
								left: 0,
								right: 0,
								top: y,
								borderTop: '1px dashed rgba(148, 163, 184, 0.25)',
								color: '#64748b',
								fontSize: 18,
								paddingLeft: 4,
								opacity: headerOpacity,
							}}
						>
							{tick}%
						</div>
					);
				})}

				{BARS.map((bar, i) => {
					// Each bar starts rising slightly after the previous one.
					const delay = 15 + i * 6;
					const grow = spring({
						fps,
						frame: frame - delay,
						config: {damping: 14, stiffness: 80, mass: 1},
					});
					const height = grow * (bar.value / MAX_VALUE) * CHART_HEIGHT;

					const valueOpacity = interpolate(
						frame,
						[delay + 18, delay + 30],
						[0, 1],
						{extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
					);
					// Count up the visible % number from 0 to its final value.
					const valueProgress = interpolate(
						frame,
						[delay, delay + 30],
						[0, bar.value],
						{extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
					);

					return (
						<div
							key={bar.industry}
							style={{
								display: 'flex',
								flexDirection: 'column',
								alignItems: 'center',
								width: 180,
								position: 'relative',
								zIndex: 1,
							}}
						>
							<div
								style={{
									color: 'white',
									fontSize: 36,
									fontWeight: 800,
									marginBottom: 12,
									opacity: valueOpacity,
								}}
							>
								{Math.round(valueProgress)}%
							</div>
							<div
								style={{
									width: 140,
									height,
									background: `linear-gradient(180deg, ${bar.color}, ${bar.color}aa)`,
									borderRadius: '12px 12px 0 0',
									boxShadow: `0 0 40px ${bar.color}55`,
								}}
							/>
							<div
								style={{
									color: '#cbd5e1',
									fontSize: 24,
									fontWeight: 600,
									marginTop: 16,
									opacity: headerOpacity,
									textAlign: 'center',
								}}
							>
								{bar.industry}
							</div>
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};
