import { useState } from "react";
import { Alert, Badge, Button, Group, Paper, Stack, Text, Title } from "@mantine/core";
import {
  IconAlertCircle,
  IconArrowRight,
  IconFileTypeJs,
  IconFolderOpen,
  IconUpload,
} from "@tabler/icons-react";
import { open } from "@tauri-apps/plugin-dialog";
import { LogUploadPanelProps } from "../types/log-upload-panel.types";
import "../styles/log-upload-panel.css";

export function LogUploadPanel({
  onAnalyze,
  isAnalyzing = false,
}: LogUploadPanelProps) {
  const [selectedPath, setSelectedPath] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleSelectFile() {
    setError(null);

    try {
      const selection = await open({
        multiple: false,
        filters: [
          {
            name: "Sensor log files",
            extensions: ["log"],
          },
        ],
      });

      if (typeof selection === "string") {
        setSelectedPath(selection);
      }
    } catch (cause) {
      setError(
        cause instanceof Error ? cause.message : String(cause),
      );
    }
  }

  function handleAnalyze() {
    if (!selectedPath || isAnalyzing) return;
    onAnalyze(selectedPath);
  }

  const fileName = selectedPath?.split(/[\\/]/).pop();

  return (
    <Paper className="upload-panel">
      <Stack className="upload-panel__content">
        <Group className="upload-panel__header">
          <Stack className="upload-panel__heading">
            <Title className="upload-panel__title" order={3}>
              Import log file
            </Title>
            <Text className="upload-panel__description">
              Select a SAMPLE-A.LOG or SAMPLE-P.LOG file.
            </Text>
          </Stack>

          <Badge
            className="upload-panel__file-badge"
            leftSection={<IconFileTypeJs size={14} />}
          >
            .LOG
          </Badge>
        </Group>

        <Paper className="upload-panel__dropzone">
          <Stack className="upload-panel__dropzone-content">
            <IconUpload
              size={32}
              stroke={1.5}
              className="upload-panel__upload-icon"
            />

            <Stack className="upload-panel__file-info">
              <Text className="upload-panel__file-name">
                {fileName ?? "Choose a log file"}
              </Text>

              <Text className="upload-panel__file-description">
                {selectedPath
                  ? "File selected"
                  : "Browse files on your computer"}
              </Text>
            </Stack>

            <Button
              className="upload-panel__browse-button"
              leftSection={<IconFolderOpen size={16} />}
              onClick={handleSelectFile}
              disabled={isAnalyzing}
            >
              Browse files
            </Button>
          </Stack>
        </Paper>

        {error && (
          <Alert
            className="upload-panel__error"
            icon={<IconAlertCircle size={18} />}
            title="File selection failed"
          >
            {error}
          </Alert>
        )}

        <Group className="upload-panel__footer">
          <Text className="upload-panel__status" role="status">
            {isAnalyzing
              ? "Analyzing log..."
              : selectedPath
                ? "File selected and ready for analysis."
                : "Select a log file to get started."}
          </Text>

          <Button
            className="upload-panel__analyze-button"
            onClick={handleAnalyze}
            disabled={!selectedPath || isAnalyzing}
            loading={isAnalyzing}
            loaderProps={{ type: "dots" }}
            rightSection={
              isAnalyzing ? undefined : <IconArrowRight size={16} />
            }
          >
            {isAnalyzing ? "Analyzing..." : "Analyze log"}
          </Button>
        </Group>
      </Stack>
    </Paper>
  );
}
