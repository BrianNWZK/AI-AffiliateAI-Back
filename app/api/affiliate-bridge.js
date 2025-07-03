import express from "express";
const app = express();
app.use(express.json());

const activities = [];

function addActivity(type, payload = {}) {
  activities.unshift({ type, ...payload, timestamp: Date.now() });
  if (activities.length > 20) activities.length = 20;
}

app.get("/affiliate/metrics", (req, res) => {
  res.json({
    activeCampaigns: 12,
    conversionRate: 3.7,
    totalClicks: 15420,
    revenue: 8750.5,
    topPerformers: [
      { name: "Tech Products Campaign", conversion: 4.2, revenue: 3200 },
      { name: "Health & Wellness", conversion: 3.8, revenue: 2800 },
      { name: "Digital Services", conversion: 3.1, revenue: 2750 },
    ],
    timestamp: new Date().toISOString(),
  });
  addActivity("metrics-served");
});

app.post("/affiliate/optimize", (req, res) => {
  addActivity("optimize-triggered", req.body);
  res.json({ success: true, message: "Affiliate optimization started!" });
});

app.get("/affiliate/activities", (req, res) => {
  res.json({ activities });
});

const PORT = process.env.PORT || 3002;
app.listen(PORT, () => {
  console.log(`Affiliate Bridge running on port ${PORT}`);
});
