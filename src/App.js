import logo from './logo.svg';
                import './App.css';

                import {WebexMeetingsWidget} from '@webex/widgets';

                import '@webex/widgets/dist/css/webex-widgets.css';

                export default function App() {
                return (
                    <WebexMeetingsWidget
                    style={{width: "1000px", height: "500px"}} // Substitute with any arbitrary size or use `className`
                    accessToken="Bearer ODMzMDQ4NTEtMGFhMi00MmY2LTk2ODItZGM2ZmE1MWY1OTUzZmMyMzk2ODEtNjE1_PE93_7075bcc6-99cf-4039-8161-d4879988024e"
                    meetingDestination= "armin@kbcg.eu"
                    />
                );
                }
                