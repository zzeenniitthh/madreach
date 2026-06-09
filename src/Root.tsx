import {Composition} from 'remotion';
import {MyComp} from './MyComp';
import {EndCard} from './EndCard';
import {RemorooEndCard} from './RemorooEndCard';
import {RequestAccessCard} from './RequestAccessCard';

export const Root: React.FC = () => {
	return (
		<>
			<Composition
				id="MyComp"
				component={MyComp}
				durationInFrames={180}
				width={1920}
				height={1080}
				fps={30}
				defaultProps={{}}
			/>
			<Composition
				id="EndCard"
				component={EndCard}
				durationInFrames={120}
				width={1920}
				height={1080}
				fps={30}
				defaultProps={{}}
			/>
			<Composition
				id="RemorooEndCard"
				component={RemorooEndCard}
				durationInFrames={120}
				width={1920}
				height={1080}
				fps={30}
				defaultProps={{}}
			/>
			<Composition
				id="RequestAccessCard"
				component={RequestAccessCard}
				durationInFrames={120}
				width={1920}
				height={1080}
				fps={30}
				defaultProps={{}}
			/>
		</>
	);
};
