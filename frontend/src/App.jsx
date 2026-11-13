import { useState, useEffect } from 'react';
import MetricsView from './components/MetricsView';
import AlertBox from './components/AlertBox';
import TrafficForm from './components/TrafficForm';

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function App() {
    const [isAnomaly, setIsAnomaly] = useState(false);
    const [metrics, setMetrics] = useState(null);

    // Load the real test-set metrics saved by the training script
    useEffect(() => {
        fetch(`${API_URL}/metrics`)
            .then((res) => res.json())
            .then((data) => setMetrics(data))
            .catch((error) => console.error("Could not load metrics:", error));
    }, []);

    const handlePrediction = (result) => {
        setIsAnomaly(result.is_anomaly);
        console.log("MSE Loss (Anomaly Score):", result.anomaly_score, "Threshold:", result.threshold);
    };

    return (
        <div className="min-h-screen bg-slate-950 text-slate-100 font-sans flex flex-col items-center py-12 px-4 sm:px-6 lg:px-8">
            <div className="w-full max-w-5xl flex flex-col gap-10 items-center">

                <div className="text-center mb-4">
                    <h1 className="text-4xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400 tracking-tight">
                        DeepAnomaly
                    </h1>
                    <p className="mt-3 text-slate-400 text-lg">Autoencoder-based Network Anomaly Detection</p>
                </div>

                <div className="w-full max-w-2xl flex flex-col gap-6">
                    <TrafficForm onPredictionResult={handlePrediction} />
                    <div className="w-full transition-all duration-500">
                        <AlertBox isAnomaly={isAnomaly} />
                    </div>
                </div>

                {metrics && (
                    <div className="w-full mt-8 pt-8 border-t border-slate-800/80 flex flex-col items-center">
                        <h2 className="text-xl font-semibold text-slate-400 mb-8 tracking-wide">
                            Model Metrics (UNSW-NB15 test set)
                        </h2>
                        <MetricsView {...metrics} />
                    </div>
                )}

            </div>
        </div>
    );
}

export default App;