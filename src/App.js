import logo from './logo.svg';
                import './App.css';

                import {WebexMeetingsWidget} from '@webex/widgets';

                import '@webex/widgets/dist/css/webex-widgets.css';

                export default function App() {
                return (
                    <WebexMeetingsWidget
                    style={{width: "1000px", height: "500px"}} // Substitute with any arbitrary size or use `className`
                    accessToken="Bearer NTQ1N2I3NjYtZTA0OC00MDcyLWJhZDEtMDQwM2ZkMzFmZWJjYmQzNmRhY2ItNzA5_PE93_7075bcc6-99cf-4039-8161-d4879988024e"
                    meetingDestination= "nickfury@kbcg.eu"
                    />
                );
                }
                