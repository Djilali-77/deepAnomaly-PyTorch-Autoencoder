import { motion } from 'framer-motion';

export default function AlertBox({ isAnomaly }) {
    if (isAnomaly) {
        return (
            <motion.div 
                animate={{ opacity: [0.4, 1, 0.4], scale: [0.98, 1.02, 0.98] }}
                transition={{ repeat: Infinity, duration: 0.8 }}
                className="w-full bg-red-900/50 border-2 border-red-500 shadow-[0_0_30px_rgba(239,68,68,0.5)] rounded-2xl p-8 text-center"
            >
                <h2 className="text-red-400 font-extrabold text-2xl tracking-widest uppercase flex items-center justify-center gap-3">
                    <span>🚨</span> CRITICAL: Anomaly Detected <span>🚨</span>
                </h2>
                <p className="text-red-200 mt-3 text-sm">
                    Malicious traffic patterns identified in the current network stream.
                </p>
            </motion.div>
        );
    }

    return (
        <div className="w-full bg-emerald-900/30 border border-emerald-500/50 rounded-2xl p-8 text-center shadow-lg transition-all duration-500">
            <h2 className="text-emerald-400 font-bold text-xl flex items-center justify-center gap-2">
                <span>✅</span> System Secure
            </h2>
            <p className="text-emerald-200/70 mt-3 text-sm">
                Network traffic is operating within normal parameters.
            </p>
        </div>
    );
}