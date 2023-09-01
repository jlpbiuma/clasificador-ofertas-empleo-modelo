import React, { useState, useEffect } from "react";
import axios from "axios";
import Plot from "react-plotly.js";
import { Slider, Tooltip, Paper, Typography } from "@material-ui/core";

function ScatterPlot() {
  const [data, setData] = useState([]);
  const [minCount, setMinCount] = useState(0);
  const [maxCount, setMaxCount] = useState(100); // Adjust the initial values
  const [minMean, setMinMean] = useState(0);
  const [maxMean, setMaxMean] = useState(100); // Adjust the initial values

  useEffect(() => {
    // Fetch data from your Python API
    axios
      .get("/api/data")
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);

  const filteredData = data.filter((item) => {
    return (
      item.Count >= minCount &&
      item.Count <= maxCount &&
      item.Mean >= minMean &&
      item.Mean <= maxMean
    );
  });

  return (
    <div>
      <h1>Scatter Plot</h1>

      {/* Range Sliders */}
      <div>
        <Typography>Count Range:</Typography>
        <Slider
          value={[minCount, maxCount]}
          onChange={(event, newValue) => {
            setMinCount(newValue[0]);
            setMaxCount(newValue[1]);
          }}
          valueLabelDisplay="auto"
          min={0}
          max={100} // Adjust the max value as needed
        />
      </div>

      <div>
        <Typography>Mean Range:</Typography>
        <Slider
          value={[minMean, maxMean]}
          onChange={(event, newValue) => {
            setMinMean(newValue[0]);
            setMaxMean(newValue[1]);
          }}
          valueLabelDisplay="auto"
          min={0}
          max={100} // Adjust the max value as needed
        />
      </div>

      {/* Scatter Plot */}
      <div>
        <Plot
          data={[
            {
              type: "scatter",
              mode: "markers",
              x: filteredData.map((item) => item.Count),
              y: filteredData.map((item) => item.Mean),
              text: filteredData.map(
                (item) =>
                  `${item.ID_PUESTO_ESCO_ULL}<br>Count: ${item.Count}<br>Mean: ${item.Mean}`
              ),
              hoverinfo: "text",
            },
          ]}
          layout={{
            title: "Scatter Plot",
            xaxis: { title: "Count" },
            yaxis: { title: "Mean" },
          }}
        />
      </div>
    </div>
  );
}

export default ScatterPlot;
