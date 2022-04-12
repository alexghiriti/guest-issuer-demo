import logo from './logo.svg';
import './App.css';

import { WebexMeetingsWidget } from '@webex/widgets';

import '@webex/widgets/dist/css/webex-widgets.css';

export default function App() {
  return (
    <WebexMeetingsWidget
      style={{ width: "1000px", height: "500px" }} // Substitute with any arbitrary size or use `className`
      accessToken="Bearer NTVjYzFmNTItMWM1NC00ZmFlLWE0NWYtN2EyYmQxMGU5ZmNkOTdhYzRkMTQtZGZl_PE93_d484b111-60e0-4056-9456-b221db552aff"
      meetingDestination="nickfury@kbcg.eu"
    />
  );
}
