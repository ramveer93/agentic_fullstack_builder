import { useState, useRef, useEffect } from 'react';
import { Play, Code, FileText, Terminal, CheckCircle, Download } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

function App() {
  const [requirements, setRequirements] = useState('');
  const [logs, setLogs] = useState<string[]>([]);
  const [isBuilding, setIsBuilding] = useState(false);
  const [activeTab, setActiveTab] = useState<'terminal' | 'codebase' | 'design' | 'preview'>('terminal');
  
  const [codebaseFiles, setCodebaseFiles] = useState<{path: string, content: string}[]>([]);
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [designCode, setDesignCode] = useState('');
  const [previewPort, setPreviewPort] = useState<number | null>(null);
  const [isPreviewLoading, setIsPreviewLoading] = useState(false);

  const logsEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  const handleBuild = async () => {
    if (!requirements.trim()) return;
    
    setLogs([]);
    setIsBuilding(true);
    setActiveTab('terminal');
    setCodebaseFiles([]);
    setSelectedFile(null);
    setDesignCode('');
    setPreviewPort(null);

    try {
      const response = await fetch('/api/build', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ requirements })
      });

      if (!response.body) throw new Error("No response body");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n').filter(l => l.trim() !== '');
        
        for (const line of lines) {
          try {
            const data = JSON.parse(line);
            if (data.log) {
              setLogs(prev => [...prev, data.log]);
            }
            if (data.status === 'completed') {
              fetchCode();
            }
          } catch (e) {
            console.error("Failed to parse log line", line);
          }
        }
      }
    } catch (error) {
      console.error("Build failed", error);
      setLogs(prev => [...prev, "ERROR: Build failed to communicate with server."]);
    } finally {
      setIsBuilding(false);
    }
  };

  const fetchCode = async () => {
    try {
      const res = await fetch('/api/code');
      const data = await res.json();
      setCodebaseFiles(data.files || []);
      if (data.files && data.files.length > 0) {
        setSelectedFile(data.files[0].path);
      }
      setDesignCode(data.design_code || '');
    } catch (e) {
      console.error("Failed to fetch code", e);
    }
  };

  const handleRunApp = async () => {
    setIsPreviewLoading(true);
    setActiveTab('preview');
    setPreviewPort(null);
    try {
      const res = await fetch('/api/run-sandbox', { method: 'POST' });
      const data = await res.json();
      if (data.port) {
        setTimeout(() => {
          setPreviewPort(data.port);
          setIsPreviewLoading(false);
        }, 3000);
      }
    } catch (e) {
      setIsPreviewLoading(false);
      console.error("Failed to run app", e);
      alert("Failed to start the sandbox app.");
    }
  };

  return (
    <div className="h-screen bg-gray-50 flex flex-col font-sans text-slate-800 overflow-hidden">
      <header className="bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center shadow-sm z-10 shrink-0">
        <h1 className="text-xl font-bold text-indigo-600 flex items-center gap-2">
          <Terminal size={24} />
          Agentic Builder
        </h1>
        <div className="text-sm text-gray-500 font-medium">Engineering Team Crew</div>
      </header>

      <main className="flex-1 max-w-7xl w-full mx-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-0 overflow-hidden">
        
        {/* Left Panel - Input */}
        <div className="lg:col-span-4 flex flex-col gap-4 h-full min-h-0">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 flex-1 flex flex-col min-h-0">
            <h2 className="font-semibold text-lg mb-2 flex items-center gap-2">
              <FileText size={18} className="text-indigo-500"/>
              Requirements
            </h2>
            <p className="text-sm text-gray-500 mb-4">Describe the application you want the AI engineering team to build.</p>
            <textarea 
              className="flex-1 w-full border border-gray-300 rounded-lg p-3 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none resize-none"
              placeholder="e.g. A simple account management system for a trading simulation platform..."
              value={requirements}
              onChange={e => setRequirements(e.target.value)}
              disabled={isBuilding}
            />
            <button 
              onClick={handleBuild}
              disabled={isBuilding || !requirements.trim()}
              className="mt-4 w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2.5 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isBuilding ? (
                <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent" />
              ) : (
                <Play size={18} />
              )}
              {isBuilding ? 'Crew is Building...' : 'Build App'}
            </button>
          </div>
        </div>

        {/* Right Panel - Output */}
        <div className="lg:col-span-8 bg-white rounded-xl shadow-sm border border-gray-200 flex flex-col h-full min-h-0 overflow-hidden">
          
          {/* Tabs */}
          <div className="flex border-b border-gray-200 bg-gray-50/50">
            <button onClick={() => setActiveTab('terminal')} className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors flex items-center gap-2 ${activeTab === 'terminal' ? 'border-indigo-600 text-indigo-600 bg-white' : 'border-transparent text-gray-600 hover:text-gray-900 hover:bg-gray-100'}`}>
              <Terminal size={16} /> Logs
            </button>
            <button onClick={() => setActiveTab('design')} className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors flex items-center gap-2 ${activeTab === 'design' ? 'border-indigo-600 text-indigo-600 bg-white' : 'border-transparent text-gray-600 hover:text-gray-900 hover:bg-gray-100'}`}>
              <FileText size={16} /> Design.md
            </button>
            <button onClick={() => setActiveTab('codebase')} className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors flex items-center gap-2 ${activeTab === 'codebase' ? 'border-indigo-600 text-indigo-600 bg-white' : 'border-transparent text-gray-600 hover:text-gray-900 hover:bg-gray-100'}`}>
              <Code size={16} /> Codebase
            </button>
            <div className="flex-1 flex justify-end items-center px-2 gap-2">
               <button 
                onClick={() => window.open('/api/download', '_blank')}
                disabled={codebaseFiles.length === 0}
                className={`text-sm px-3 py-1.5 rounded-md font-medium flex items-center gap-1.5 transition-colors ${codebaseFiles.length > 0 ? 'bg-indigo-100 text-indigo-700 hover:bg-indigo-200' : 'bg-gray-100 text-gray-400 cursor-not-allowed'}`}
                title="Download Codebase"
              >
                <Download size={14} /> Download
              </button>
               <button 
                onClick={handleRunApp}
                disabled={codebaseFiles.length === 0}
                className={`text-sm px-3 py-1.5 rounded-md font-medium flex items-center gap-1.5 transition-colors ${codebaseFiles.length > 0 ? 'bg-green-100 text-green-700 hover:bg-green-200' : 'bg-gray-100 text-gray-400 cursor-not-allowed'}`}
              >
                <Play size={14} /> Run Sandbox
              </button>
            </div>
            {previewPort && (
              <button onClick={() => setActiveTab('preview')} className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors flex items-center gap-2 ${activeTab === 'preview' ? 'border-green-500 text-green-600 bg-white' : 'border-transparent text-gray-600 hover:text-gray-900 hover:bg-gray-100'}`}>
                Preview
              </button>
            )}
          </div>

          {/* Content Area */}
          <div className="flex-1 overflow-hidden relative bg-gray-50 min-h-0">
            {activeTab === 'terminal' && (
              <div className="h-full overflow-y-auto bg-[#1e1e1e] p-4 font-mono text-sm text-gray-300">
                {logs.length === 0 && !isBuilding ? (
                  <div className="text-gray-500 text-center mt-10 italic">Awaiting instructions...</div>
                ) : (
                  logs.map((log, i) => (
                    <div key={i} className="mb-1">{log}</div>
                  ))
                )}
                <div ref={logsEndRef} />
              </div>
            )}
            
            {activeTab === 'codebase' && (
              <div className="flex h-full min-h-0 bg-[#1e1e1e]">
                {/* File Explorer Sidebar */}
                <div className="w-64 border-r border-[#333] flex flex-col bg-[#252526] overflow-y-auto">
                  <div className="px-4 py-2 text-xs font-semibold text-gray-400 uppercase tracking-wider sticky top-0 bg-[#252526]">
                    Files
                  </div>
                  <div className="flex flex-col py-1">
                    {codebaseFiles.map(file => (
                      <button
                        key={file.path}
                        onClick={() => setSelectedFile(file.path)}
                        className={`text-left px-4 py-1.5 text-sm font-mono truncate flex items-center gap-2 ${selectedFile === file.path ? 'bg-[#37373d] text-white' : 'text-gray-400 hover:bg-[#2a2d2e] hover:text-gray-300'}`}
                        title={file.path}
                      >
                        <FileText size={14} className="shrink-0" />
                        <span className="truncate">{file.path}</span>
                      </button>
                    ))}
                  </div>
                </div>
                {/* Code Editor Area */}
                <div className="flex-1 overflow-auto p-4">
                  {selectedFile ? (
                    <pre className="font-mono text-sm text-green-400 whitespace-pre-wrap">
                      {codebaseFiles.find(f => f.path === selectedFile)?.content || ''}
                    </pre>
                  ) : (
                    <div className="text-gray-500 text-center mt-10 italic">Select a file to view</div>
                  )}
                </div>
              </div>
            )}

            {activeTab === 'design' && (
              <div className="h-full overflow-y-auto p-6 bg-white max-w-none">
                <div className="prose prose-indigo max-w-none">
                  {designCode ? <ReactMarkdown>{designCode}</ReactMarkdown> : <div className="text-gray-500 font-mono text-sm">No design generated yet.</div>}
                </div>
              </div>
            )}



            {activeTab === 'preview' && (
              <div className="h-full bg-white flex flex-col">
                {isPreviewLoading ? (
                  <div className="flex-1 flex items-center justify-center text-gray-500 flex-col gap-4">
                    <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
                    <div>Starting Sandbox Server...</div>
                  </div>
                ) : previewPort ? (
                  <iframe 
                    src={`http://127.0.0.1:${previewPort}`} 
                    className="w-full h-full border-0"
                    title="Sandbox Preview"
                  />
                ) : (
                  <div className="flex-1 flex items-center justify-center text-gray-500">
                    No preview available. Click "Run Sandbox".
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
