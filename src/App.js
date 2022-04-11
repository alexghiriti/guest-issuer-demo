import logo from './logo.svg';
import './App.css';

import {WebexMeetingsWidget} from '@webex/widgets';

import '@webex/widgets/dist/css/webex-widgets.css';

export default function App() {
  return (
    <WebexMeetingsWidget
      style={{width: "1000px", height: "500px"}} // Substitute with any arbitrary size or use `className`
      accessToken="Bearer Y2QyY2RkNGYtZWM4NC00MDIyLWEwYjMtNWU0OGMwNDQyOTc2ZWQ4NjEwZjAtNjhm_PE93_298d3c23-9d31-4483-9cfa-1e6a5288cf32"
      meetingDestination="tino@kbcg.eu"
    />
  );
}
