const BOT_API = process.env.VUE_APP_BOT_API;

export default {
    home: `${window.location.origin}/`,
    botApi: BOT_API || "",
    colors: {
        default: "#344675",
        primary: "#42b883",
        info: "#1d8cf8",
        danger: "#fd5d93",
        teal: "#00d6b4",
        primaryGradient: ['rgba(66,134,121,0.55)', 'rgba(66,134,121,0.05)', 'rgba(66,134,121,0)'],
    }
}