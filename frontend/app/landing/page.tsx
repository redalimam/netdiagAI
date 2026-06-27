export default function Landing() {
  const features = [
    { icon: "🔍", title: "Scan Intelligent", desc: "Analyse complete de vos reseaux en quelques secondes." },
    { icon: "🤖", title: "Diagnostic IA", desc: "Notre IA transforme les donnees brutes en rapports clairs." },
    { icon: "🔔", title: "Alertes Instantanees", desc: "Recevez un email des qu'un probleme est detecte." },
  ];

  const plans = [
    { name: "Starter", price: "0", desc: "Pour commencer", features: ["1 reseau", "Scan manuel", "Rapport IA basique"], featured: false },
    { name: "Pro", price: "29", desc: "Le plus populaire", features: ["5 reseaux", "Scan automatique", "Alertes email", "Rapport IA complet"], featured: true },
    { name: "Business", price: "89", desc: "Pour les equipes", features: ["Reseaux illimites", "Scan toutes les 5 min", "Alertes Slack", "Export PDF"], featured: false },
  ];

  return (
    <main className="min-h-screen bg-gray-950 text-white">

      <div className="max-w-4xl mx-auto px-6 pt-20 pb-16 text-center">
        <div className="inline-block bg-blue-950 text-blue-400 text-sm px-4 py-1 rounded-full mb-6">
          Propulse par IA
        </div>
        <h1 className="text-5xl font-bold mb-6 leading-tight">
          Surveillez votre reseau.<br />
          <span className="text-blue-400">L'IA s'occupe du reste.</span>
        </h1>
        <p className="text-xl text-gray-400 mb-10 max-w-2xl mx-auto">
          NetDiagAI analyse vos infrastructures reseau, detecte les problemes
          et vous envoie des rapports intelligents en temps reel.
        </p>
        <div className="flex gap-4 justify-center">
          <a href="/" className="bg-blue-600 hover:bg-blue-700 px-8 py-4 rounded-xl font-semibold text-lg transition-colors">
            Essayer gratuitement
          </a>
          <a href="#features" className="bg-gray-800 hover:bg-gray-700 px-8 py-4 rounded-xl font-semibold text-lg transition-colors">
            En savoir plus
          </a>
        </div>
      </div>

      <div id="features" className="max-w-4xl mx-auto px-6 py-16">
        <h2 className="text-3xl font-bold text-center mb-12">Tout ce dont vous avez besoin</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {features.map((f, i) => (
            <div key={i} className="bg-gray-900 rounded-2xl p-6 border border-gray-800">
              <div className="text-4xl mb-4">{f.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{f.title}</h3>
              <p className="text-gray-400">{f.desc}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-6 py-16">
        <h2 className="text-3xl font-bold text-center mb-12">Tarifs simples</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {plans.map((p, i) => (
            <div key={i} className={`rounded-2xl p-6 border ${p.featured ? "border-blue-500 bg-blue-950" : "border-gray-800 bg-gray-900"}`}>
              <div className="text-lg font-semibold mb-1">{p.name}</div>
              <div className="text-4xl font-bold mb-1">
                ${p.price}<span className="text-lg text-gray-400">/mois</span>
              </div>
              <div className="text-gray-400 text-sm mb-6">{p.desc}</div>
              <ul className="space-y-2">
                {p.features.map((feat, j) => (
                  <li key={j} className="flex items-center gap-2 text-sm">
                    <span className="text-green-400">V</span> {feat}
                  </li>
                ))}
              </ul>
              <a href="/" className={`block text-center mt-6 py-3 rounded-xl font-medium transition-colors ${p.featured ? "bg-blue-600 hover:bg-blue-700" : "bg-gray-700 hover:bg-gray-600"}`}>
                Commencer
              </a>
            </div>
          ))}
        </div>
      </div>

      <div className="text-center py-8 text-gray-600 text-sm border-t border-gray-800">
        NetDiagAI — Fait avec passion par un etudiant ENSTTIC
      </div>

    </main>
  );
}