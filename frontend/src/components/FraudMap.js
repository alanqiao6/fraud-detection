import React, { useEffect, useState } from "react";
import axios from "axios";
import { ComposableMap, Geographies, Geography } from "react-simple-maps";
import { scaleLinear } from "d3-scale";

const geoUrl =
  "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json";

const FraudMap = () => {
  const [data, setData] = useState([]);
  const [tooltipContent, setTooltipContent] = useState("");

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/fraud_map")
      .then(res => setData(res.data))
      .catch(err => console.error(err));
  }, []);

  const fraudMap = {};
  data.forEach(d => {
    if (d.countryName) {
      fraudMap[d.countryName.toLowerCase()] = {
        fraud: d.fraud,
        total: d.total
      };
    }
  });

  const maxRate = Math.max(
    ...data.map(d => (d.fraud / d.total) * 100 || 0),
    1
  );

  const colorScale = scaleLinear()
    .domain([0, maxRate])
    .range(["#f0f0f0", "#8b0000"]);  // light → dark red

  return (
    <div>
      <h3>Fraud by Geography</h3>
      <ComposableMap
        projectionConfig={{ scale: 100 }}  // ↓ smaller map
        width={800}
        height={400}
      >
        <Geographies geography={geoUrl}>
          {({ geographies }) =>
            geographies.map(geo => {
              const name = geo.properties.name.toLowerCase();
              const info = fraudMap[name];
              const fraudRate = info ? (info.fraud / info.total) * 100 : 0;

              return (
                <Geography
                  key={geo.rsmKey}
                  geography={geo}
                  fill={fraudRate > 0 ? colorScale(fraudRate) : "#EEE"}
                  onMouseEnter={() => {
                    setTooltipContent(
                      `${geo.properties.name}: ${info?.fraud || 0} fraud / ${info?.total || 0} logs (${fraudRate.toFixed(2)}%)`
                    );
                  }}
                  onMouseLeave={() => {
                    setTooltipContent("");
                  }}
                  style={{
                    default: { outline: "none" },
                    hover: { fill: "#d7191c", outline: "none" },
                    pressed: { outline: "none" },
                  }}
                />
              );
            })
          }
        </Geographies>
      </ComposableMap>
      <div style={{ marginTop: "10px" }}>
        {tooltipContent || "Hover over a country to see details"}
      </div>
    </div>
  );
};

export default FraudMap;
