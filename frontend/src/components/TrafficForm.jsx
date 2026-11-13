import { useState } from 'react';

export default function TrafficForm({ onPredictionResult }) {
    const [formData, setFormData] = useState({
        sttl: 31,
        ct_state_ttl: 0,
        sbytes: 500,
        dbytes: 1200,
        smean: 64
    });
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: Number(e.target.value) });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        
        try {
            // Use environment variable, fallback to localhost for local dev
            const apiUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
            
            const response = await fetch(`${apiUrl}/predict`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData)
            });
            const result = await response.json();
            onPredictionResult(result);
        } catch (error) {
            console.error("API Error:", error);
            alert("Error connecting to Backend API! (Check if FastAPI is running)");
        } finally {
            setLoading(false);
        }
    };
    return (
        <form onSubmit={handleSubmit} className="bg-slate-800 border border-slate-700 p-6 rounded-2xl shadow-xl w-full">
            <h3 className="text-lg font-semibold text-slate-200 mb-5 border-b border-slate-700 pb-3">
                Network Packet Simulator
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                {Object.keys(formData).map((key) => (
                    <div key={key} className="flex flex-col gap-1">
                        <label className="text-slate-400 text-xs font-bold uppercase tracking-wider">{key}</label>
                        <input 
                            type="number" 
                            name={key} 
                            value={formData[key]} 
                            onChange={handleChange} 
                            className="bg-slate-900 border border-slate-600 text-slate-100 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all" 
                        />
                    </div>
                ))}
            </div>
            
            <button 
                type="submit" 
                disabled={loading}
                className="hover:cursor-pointer w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 px-4 rounded-lg transition-colors flex justify-center items-center gap-2 disabled:opacity-50"
            >
                {loading ? 'Analyzing Traffic...' : 'Analyze Traffic 🚀'}
            </button>
        </form>
    );
}