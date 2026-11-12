export default function MetricsView({ accuracy, precision, recall, f1 }) {
    const metrics = [
        { label: 'Accuracy', value: accuracy },
        { label: 'Precision', value: precision },
        { label: 'Recall', value: recall },
        { label: 'F1-Score', value: f1 }
    ];

    return (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 w-full">
            {metrics.map((metric, idx) => (
                <div key={idx} className="bg-slate-800 border border-slate-700 shadow-lg rounded-xl p-4 flex flex-col items-center justify-center transition-transform hover:scale-105">
                    <h3 className="text-slate-400 text-sm uppercase tracking-wider mb-1">{metric.label}</h3>
                    <p className="text-emerald-400 text-2xl font-bold">
                        {(metric.value * 100).toFixed(2)}%
                    </p>
                </div>
            ))}
        </div>
    );
}