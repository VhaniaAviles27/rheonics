import { Plot } from "../../../lib/plotly-factory";
import type { PlotlyFigure } from "../types/plots.types";
import "../styles/plot-viewer.css";

interface PlotlyChartProps {
  figure: PlotlyFigure;
}

export function PlotlyChart({ figure }: PlotlyChartProps) {
  return (
    <div className="plot-viewer__chart">
      <Plot
        data={figure.data as never[]}
        layout={{
          ...(figure.layout as object),
          autosize: true,
        }}
        config={{
          responsive: true,
          displaylogo: false,
          modeBarButtonsToRemove: ["lasso2d", "select2d"],
        }}
        style={{ width: "100%", height: "100%" }}
        useResizeHandler
      />
    </div>
  );
}