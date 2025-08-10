'use client'

import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  DocumentTextIcon,
  SparklesIcon,
  ChatBubbleLeftRightIcon,
  BookmarkIcon,
  ShareIcon,
  Cog6ToothIcon,
  PlusIcon,
  ChevronDownIcon,
  ChevronRightIcon,
  EyeIcon,
  PencilIcon,
  BoltIcon,
  LightBulbIcon
} from '@heroicons/react/24/outline'
import ReactMarkdown from 'react-markdown'

interface Chapter {
  id: string
  title: string
  content: string
  wordCount: number
  isExpanded?: boolean
  subsections?: Chapter[]
}

interface AIMessage {
  id: string
  type: 'user' | 'assistant'
  content: string
  timestamp: string
}

export default function EditorPage({ params }: { params: { id: string } }) {
  const [book, setBook] = useState({
    id: params.id,
    title: 'React 高级开发指南',
    description: '深入探讨React生态系统的高级概念和最佳实践'
  })
  
  const [chapters, setChapters] = useState<Chapter[]>([
    {
      id: '1',
      title: '第一章：React 核心概念',
      content: '# React 核心概念\n\nReact 是一个用于构建用户界面的 JavaScript 库...',
      wordCount: 1200,
      isExpanded: true,
      subsections: [
        { id: '1-1', title: '1.1 组件化思想', content: '', wordCount: 300 },
        { id: '1-2', title: '1.2 虚拟DOM原理', content: '', wordCount: 450 },
      ]
    },
    {
      id: '2',
      title: '第二章：状态管理',
      content: '',
      wordCount: 800,
      isExpanded: false,
    },
    {
      id: '3',
      title: '第三章：性能优化',
      content: '',
      wordCount: 0,
      isExpanded: false,
    }
  ])
  
  const [activeChapter, setActiveChapter] = useState<string>('1')
  const [editorMode, setEditorMode] = useState<'write' | 'preview'>('write')
  const [showAIAssistant, setShowAIAssistant] = useState(false)
  const [aiMessages, setAiMessages] = useState<AIMessage[]>([
    {
      id: '1',
      type: 'assistant',
      content: '你好！我是你的AI写作助手。我可以帮助你：\n\n• 生成章节大纲\n• 扩展内容要点\n• 优化文字表达\n• 提供技术见解\n\n有什么我可以帮助你的吗？',
      timestamp: '10:30'
    }
  ])
  const [aiInput, setAiInput] = useState('')
  const [isAiThinking, setIsAiThinking] = useState(false)
  
  const editorRef = useRef<HTMLTextAreaElement>(null)
  const aiChatRef = useRef<HTMLDivElement>(null)

  const currentChapter = chapters.find(c => c.id === activeChapter)

  const handleChapterToggle = (chapterId: string) => {
    setChapters(chapters.map(chapter => 
      chapter.id === chapterId 
        ? { ...chapter, isExpanded: !chapter.isExpanded }
        : chapter
    ))
  }

  const handleContentChange = (content: string) => {
    setChapters(chapters.map(chapter => 
      chapter.id === activeChapter 
        ? { ...chapter, content, wordCount: content.split(/\s+/).length }
        : chapter
    ))
  }

  const handleAiSubmit = async () => {
    if (!aiInput.trim()) return
    
    const userMessage: AIMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: aiInput,
      timestamp: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
    }
    
    setAiMessages([...aiMessages, userMessage])
    setAiInput('')
    setIsAiThinking(true)
    
    // 模拟AI响应
    setTimeout(() => {
      const aiResponse: AIMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: '基于你的问题，我建议从以下几个方面来展开这个章节：\n\n1. **核心概念解释**：先定义关键术语\n2. **实际应用场景**：提供具体的使用案例\n3. **最佳实践**：分享业界认可的做法\n4. **常见陷阱**：指出需要避免的问题\n\n你希望我帮你详细展开哪个部分？',
        timestamp: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
      }
      setAiMessages(prev => [...prev, aiResponse])
      setIsAiThinking(false)
    }, 2000)
  }

  const quickActions = [
    { 
      icon: LightBulbIcon, 
      label: '生成大纲', 
      action: () => setAiInput('请帮我为当前章节生成详细大纲'),
      color: 'text-yellow-600 bg-yellow-50 hover:bg-yellow-100',
      description: '让AI帮你理清思路'
    },
    { 
      icon: PencilIcon, 
      label: '扩展内容', 
      action: () => setAiInput('请帮我扩展当前段落的内容'),
      color: 'text-blue-600 bg-blue-50 hover:bg-blue-100',
      description: '丰富你的表达'
    },
    { 
      icon: BoltIcon, 
      label: '优化表达', 
      action: () => setAiInput('请帮我优化这段文字的表达方式'),
      color: 'text-purple-600 bg-purple-50 hover:bg-purple-100',
      description: '让文字更精准'
    },
  ]

  // 智能写作建议
  const [writingSuggestions, setWritingSuggestions] = useState([
    '当前章节可以添加一个实际案例来说明概念',
    '建议在开头增加一个引人入胜的问题',
    '可以考虑添加一个小结来总结要点'
  ])

  // 写作进度跟踪
  const [todayWordCount, setTodayWordCount] = useState(0)
  const [writingStreak, setWritingStreak] = useState(7) // 连续写作天数

  useEffect(() => {
    if (aiChatRef.current) {
      aiChatRef.current.scrollTop = aiChatRef.current.scrollHeight
    }
  }, [aiMessages])

  return (
    <div className="h-screen flex bg-gray-50">
      {/* 左侧边栏 - 章节导航 */}
      <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center justify-between mb-2">
            <h1 className="text-lg font-semibold text-gray-900 truncate">
              {book.title}
            </h1>
            <button className="p-1 text-gray-400 hover:text-gray-600">
              <Cog6ToothIcon className="h-5 w-5" />
            </button>
          </div>
          <p className="text-sm text-gray-600">{book.description}</p>
        </div>
        
        <div className="flex-1 overflow-y-auto">
          <div className="p-4">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-sm font-medium text-gray-900">章节目录</h2>
              <button className="p-1 text-gray-400 hover:text-gray-600">
                <PlusIcon className="h-4 w-4" />
              </button>
            </div>
            
            <div className="space-y-1">
              {chapters.map((chapter) => (
                <div key={chapter.id}>
                  <div 
                    className={`flex items-center p-2 rounded-lg cursor-pointer transition-colors ${
                      activeChapter === chapter.id 
                        ? 'bg-primary-50 text-primary-700' 
                        : 'text-gray-700 hover:bg-gray-50'
                    }`}
                    onClick={() => setActiveChapter(chapter.id)}
                  >
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        handleChapterToggle(chapter.id)
                      }}
                      className="mr-2 p-0.5"
                    >
                      {chapter.subsections ? (
                        chapter.isExpanded ? (
                          <ChevronDownIcon className="h-4 w-4" />
                        ) : (
                          <ChevronRightIcon className="h-4 w-4" />
                        )
                      ) : (
                        <div className="w-4 h-4" />
                      )}
                    </button>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium truncate">{chapter.title}</p>
                      <p className="text-xs text-gray-500">{chapter.wordCount} 字</p>
                    </div>
                  </div>
                  
                  {chapter.subsections && chapter.isExpanded && (
                    <div className="ml-6 mt-1 space-y-1">
                      {chapter.subsections.map((subsection) => (
                        <div
                          key={subsection.id}
                          className={`flex items-center p-2 rounded-lg cursor-pointer transition-colors ${
                            activeChapter === subsection.id 
                              ? 'bg-primary-50 text-primary-700' 
                              : 'text-gray-600 hover:bg-gray-50'
                          }`}
                          onClick={() => setActiveChapter(subsection.id)}
                        >
                          <div className="flex-1 min-w-0">
                            <p className="text-sm truncate">{subsection.title}</p>
                            <p className="text-xs text-gray-500">{subsection.wordCount} 字</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
        
        <div className="p-4 border-t border-gray-200">
          <button 
            onClick={() => setShowAIAssistant(!showAIAssistant)}
            className={`w-full flex items-center justify-center space-x-2 p-3 rounded-lg transition-colors ${
              showAIAssistant 
                ? 'bg-primary-600 text-white' 
                : 'bg-primary-50 text-primary-600 hover:bg-primary-100'
            }`}
          >
            <SparklesIcon className="h-5 w-5" />
            <span className="font-medium">AI 写作助手</span>
          </button>
        </div>
      </div>

      {/* 主编辑区域 */}
      <div className="flex-1 flex flex-col">
        {/* 编辑器工具栏 */}
        <div className="bg-white border-b border-gray-200 px-6 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <h2 className="text-lg font-medium text-gray-900">
                {currentChapter?.title || '选择章节'}
              </h2>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setEditorMode('write')}
                  className={`px-3 py-1 text-sm font-medium rounded-md transition-colors ${
                    editorMode === 'write' 
                      ? 'bg-primary-100 text-primary-700' 
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <PencilIcon className="h-4 w-4 inline mr-1" />
                  编辑
                </button>
                <button
                  onClick={() => setEditorMode('preview')}
                  className={`px-3 py-1 text-sm font-medium rounded-md transition-colors ${
                    editorMode === 'preview' 
                      ? 'bg-primary-100 text-primary-700' 
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <EyeIcon className="h-4 w-4 inline mr-1" />
                  预览
                </button>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-500">
                {currentChapter?.wordCount || 0} 字
              </span>
              <button className="p-2 text-gray-400 hover:text-gray-600">
                <BookmarkIcon className="h-5 w-5" />
              </button>
              <button className="p-2 text-gray-400 hover:text-gray-600">
                <ShareIcon className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>

        {/* 编辑器内容区 */}
        <div className="flex-1 flex">
          <div className="flex-1 p-6">
            {editorMode === 'write' ? (
              <textarea
                ref={editorRef}
                value={currentChapter?.content || ''}
                onChange={(e) => handleContentChange(e.target.value)}
                placeholder="开始你的创作之旅...

你可以：
• 直接输入内容
• 使用 Markdown 语法
• 随时呼叫 AI 助手获得帮助

专注于你的想法，让技术为思想服务。"
                className="w-full h-full resize-none border-none focus:outline-none text-gray-900 leading-relaxed text-lg font-serif"
                style={{ fontFamily: 'var(--font-crimson), Georgia, serif' }}
              />
            ) : (
              <div className="h-full overflow-y-auto prose-custom">
                <ReactMarkdown>
                  {currentChapter?.content || '# 开始创作\n\n选择左侧章节开始编辑，或创建新的章节。'}
                </ReactMarkdown>
              </div>
            )}
          </div>

          {/* AI 助手面板 */}
          <AnimatePresence>
            {showAIAssistant && (
              <motion.div
                initial={{ width: 0, opacity: 0 }}
                animate={{ width: 400, opacity: 1 }}
                exit={{ width: 0, opacity: 0 }}
                transition={{ duration: 0.3 }}
                className="bg-white border-l border-gray-200 flex flex-col"
              >
                <div className="p-4 border-b border-gray-200">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-medium text-gray-900">AI 写作助手</h3>
                    <button
                      onClick={() => setShowAIAssistant(false)}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      ×
                    </button>
                  </div>
                  
                  {/* 智能写作助手 */}
                  <div className="space-y-4">
                    {/* 今日写作统计 */}
                    <div className="bg-gradient-to-r from-green-50 to-blue-50 p-3 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-gray-700">今日写作</span>
                        <span className="text-xs text-gray-500">{writingStreak} 天连续</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className="flex-1 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-green-500 h-2 rounded-full transition-all duration-300"
                            style={{ width: `${Math.min(100, (todayWordCount / 1000) * 100)}%` }}
                          ></div>
                        </div>
                        <span className="text-sm font-medium text-gray-700">
                          {todayWordCount}/1000 字
                        </span>
                      </div>
                    </div>

                    {/* 快速操作 */}
                    <div className="space-y-2">
                      <p className="text-sm text-gray-600 mb-3">AI 助手：</p>
                      {quickActions.map((action, index) => (
                        <button
                          key={index}
                          onClick={action.action}
                          className={`w-full flex items-start space-x-3 p-3 rounded-lg text-sm transition-colors ${action.color} group`}
                        >
                          <action.icon className="h-4 w-4 mt-0.5 group-hover:scale-110 transition-transform" />
                          <div className="text-left">
                            <div className="font-medium">{action.label}</div>
                            <div className="text-xs opacity-75 mt-1">{action.description}</div>
                          </div>
                        </button>
                      ))}
                    </div>

                    {/* 智能建议 */}
                    <div className="border-t border-gray-200 pt-4">
                      <p className="text-sm text-gray-600 mb-3">💡 写作建议：</p>
                      <div className="space-y-2">
                        {writingSuggestions.slice(0, 2).map((suggestion, index) => (
                          <div key={index} className="p-2 bg-yellow-50 rounded text-xs text-yellow-800 border border-yellow-200">
                            {suggestion}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                {/* 对话区域 */}
                <div 
                  ref={aiChatRef}
                  className="flex-1 overflow-y-auto p-4 space-y-4"
                >
                  {aiMessages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-[80%] p-3 rounded-lg ${
                          message.type === 'user'
                            ? 'bg-primary-600 text-white'
                            : 'bg-gray-100 text-gray-900'
                        }`}
                      >
                        <div className="text-sm whitespace-pre-wrap">
                          {message.content}
                        </div>
                        <div className={`text-xs mt-1 ${
                          message.type === 'user' ? 'text-primary-100' : 'text-gray-500'
                        }`}>
                          {message.timestamp}
                        </div>
                      </div>
                    </div>
                  ))}
                  
                  {isAiThinking && (
                    <div className="flex justify-start">
                      <div className="bg-gray-100 text-gray-900 p-3 rounded-lg">
                        <div className="flex items-center space-x-2">
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600"></div>
                          <span className="text-sm">AI 正在思考<span className="loading-dots"></span></span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {/* 输入区域 */}
                <div className="p-4 border-t border-gray-200">
                  <div className="flex space-x-2">
                    <input
                      type="text"
                      value={aiInput}
                      onChange={(e) => setAiInput(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleAiSubmit()}
                      placeholder="向 AI 助手提问..."
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
                    />
                    <button
                      onClick={handleAiSubmit}
                      disabled={!aiInput.trim() || isAiThinking}
                      className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      <ChatBubbleLeftRightIcon className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  )
}