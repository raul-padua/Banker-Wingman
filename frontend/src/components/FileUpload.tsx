import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { ArrowUpTrayIcon } from '@heroicons/react/24/outline';
import { uploadFile } from '@/lib/api';
import { useAppContext } from '@/contexts/AppContext';

export default function FileUpload() {
  const {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    uploadedFileName, // This is read by PageContent, ESLint can't see that
    setUploadedFileName,
    isUploading,
    setIsUploading,
    uploadError,
    setUploadError,
    uploadSuccessMessage,
    setUploadSuccessMessage
  } = useAppContext();

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    const apiKey = localStorage.getItem('apiKey');
    if (!apiKey) {
      setUploadError('Please enter your OpenAI API key in the field above to upload files.');
      setUploadedFileName(null);
      setUploadSuccessMessage(null);
      return;
    }

    setIsUploading(true);
    setUploadError(null);
    setUploadSuccessMessage(null);

    try {
      const response = await uploadFile(file);
      if (response.error) {
        if (response.error.includes('API key')) {
          setUploadError('Invalid API key. Please check your API key and try again.');
        } else {
          setUploadError(response.error);
        }
        setUploadedFileName(null);
      } else if (response.data) {
        setUploadSuccessMessage(`Successfully uploaded ${response.data.filename} (${response.data.chunks} chunks)`);
        setUploadedFileName(response.data.filename);
        setUploadError(null);
      }
    } catch {
      setUploadError('Failed to upload file');
      setUploadedFileName(null);
    } finally {
      setIsUploading(false);
    }
  }, [setUploadedFileName, setIsUploading, setUploadError, setUploadSuccessMessage]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    maxFiles: 1
  });

  return (
    <div className="w-full max-w-xl mx-auto">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400'}`}
      >
        <input {...getInputProps()} />
        <ArrowUpTrayIcon className="mx-auto h-12 w-12 text-gray-400" />
        <p className="mt-2 text-sm text-gray-600">
          {isDragActive
            ? 'Drop the PDF file here'
            : 'Drag and drop a PDF file here, or click to select'}
        </p>
        {isUploading && (
          <p className="mt-2 text-sm text-blue-600">Uploading...</p>
        )}
        {uploadError && (
          <p className="mt-2 text-sm text-red-600">{uploadError}</p>
        )}
        {uploadSuccessMessage && !isUploading && (
          <p className="mt-2 text-sm text-green-600">{uploadSuccessMessage}</p>
        )}
      </div>
    </div>
  );
} 