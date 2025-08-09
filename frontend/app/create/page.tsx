'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  BookOpenIcon,
  SparklesIcon,
  DocumentTextIcon,
  UserGroupIcon,
  ClockIcon,
  ArrowRightIcon,
  ArrowLeftIcon,
  CheckIcon,
  LightBulbIcon,
  PencilSquareIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

interface BookTemplate {
  id: string
  name: string
  description: string
  icon: any
  color: string
  bgColor: string
  chapters: string[]
  estimatedTime: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
}

export default function CreateBookPage() {
  const router = useRouter()
  const [currentStep, setCurrentStep] = useState(1)
  const [bookData, setBookData] = useState({
    title: '',
    description: '',
    targetAudience: '',
    mainGoal: '',
    keyTopics: [] as string[],
    template: null as BookTemplate | null,
    writingStyle: 'technical' as 'technical' | 'academic' | 'practical' | 'conversational'
  })

  const templates: BookTemplate[] = [
    {
      id: 'technical-guide',
      name: '技术指南',
      description: '深入的技术教程和最佳实践指南',
      icon: DocumentTextIcon,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      chapters: ['基础概念', '核心原理', '实践应用', '高级技巧', '案例研究'],
      estimatedTime: '4-6 周',
      difficulty: 'intermediate'
    },
    {
      id: 'architecture-design',
      name: '架构设计',
      description: '系统架构和设计模式的深度解析',
      icon: ChartBarIcon,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
      chapters: ['设计原则', '架构模式', '系统设计', '性能优化', '实战案例'],
      estimatedTime: '6-8 周',
      difficulty: 'advanced'
    },
    {
      id: 'practical-handbook',
      name: '实践手册',
      description: '注重实际操作的实用指南',
      icon: PencilSquareIcon,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
      chapters: ['快速入门', '常用技巧', '问题解决', '工具使用', '项目实战'],
      estimatedTime: '3-4 周',
      difficulty: 'beginner'
    },
    {
      id: 'research-paper',
      name: '研究报告',
      description: '学术性的深度研究和分析',
      icon: LightBulbIcon,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-50',
      chapters: ['研究背景', '文献综述', '方法论', '实验结果', '结论展望'],
      estimatedTime: '8-12 周',
      difficulty: 'advanced'
    }
  ]

  const steps = [
    { id: 1, name: '基本信息', description: '告诉我们你想写什么' },
    { id: 2, name: '选择模板', description: '选择适合的图书结构' },
    { id: 3, name: '详细设置', description: '完善创作细节' },
    { id: 4, name: '确认创建', description: '开始你的创作之旅' }
  ]

  const writingStyles = [
    { id: 'technical', name: '技术性', description: '专业术语丰富，逻辑严谨' },
    { id: 'academic', name: '学术性', description: '引用文献，论证充分' },
    { id: 'practical', name: '实用性', description: '注重实践，案例丰富' },
    { id: 'conversational', name: '对话式', description: '轻松易懂，贴近读者' }
  ]

  const handleNext = () => {
    if (currentStep < 4) {
      setCurrentStep(currentStep + 1)
    }
  }

  const handlePrevious = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
    }
  }

  const handleCreateBook = async () => {
    // 这里会调用API创建图书
    console.log('Creating book with data:', bookData)
    
    // 模拟创建过程
    setTimeout(() => {
      router.push('/editor/new-book-id')
    }, 1000)
  }

  const addKeyTopic = (topic: string) => {
    if (topic && !bookData.keyTopics.includes(topic)) {
      setBookData({
        ...bookData,
        keyTopics: [...bookData.keyTopics, topic]
      })
    }
  }

  const removeKeyTopic = (topic: string) => {
    setBookData({
      ...bookData,
      keyTopics: bookData.keyTopics.filter(t => t !== topic)
    })
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'text-green-600 bg-green-100'
      case 'intermediate': return 'text-yellow-600 bg-yellow-100'
      case 'advanced': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getDifficultyText = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return '入门'
      case 'intermediate': return '中级'
      case 'advanced': return '高级'
      default: return '未知'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 顶部导航 */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/dashboard" className="flex items-center space-x-2">
              <BookOpenIcon className="h-8 w-8 text-primary-600" />
              <span className="text-xl font-bold text-gray-900">BookAgent</span>
            </Link>
            <div className="text-sm text-gray-600">
              创建新图书
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 进度指示器 */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            {steps.map((step, index) => (
              <div key={step.id} className="flex items-center">
                <div className={`flex items-center justify-center w-10 h-10 rounded-full border-2 ${
                  currentStep >= step.id 
                    ? 'bg-primary-600 border-primary-600 text-white' 
                    : 'border-gray-300 text-gray-400'
                }`}>
                  {currentStep > step.id ? (
                    <CheckIcon className="h-6 w-6" />
                  ) : (
                    <span className="text-sm font-medium">{step.id}</span>
                  )}
                </div>
                <div className="ml-3">
                  <p className={`text-sm font-medium ${
                    currentStep >= step.id ? 'text-gray-900' : 'text-gray-400'
                  }`}>
                    {step.name}
                  </p>
                  <p className="text-xs text-gray-500">{step.description}</p>
                </div>
                {index < steps.length - 1 && (
                  <div className={`flex-1 h-0.5 mx-4 ${
                    currentStep > step.id ? 'bg-primary-600' : 'bg-gray-300'
                  }`} />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* 步骤内容 */}
        <div className="card min-h-[500px]">
          <AnimatePresence mode="wait">
            {currentStep === 1 && (
              <motion.div
                key="step1"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-6"
              >
                <div className="text-center mb-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">
                    告诉我们你的想法
                  </h2>
                  <p className="text-gray-600">
                    让我们了解你想要创作的图书，AI 将帮助你完善创作思路
                  </p>
                </div>

                <div className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      图书标题 *
                    </label>
                    <input
                      type="text"
                      value={bookData.title}
                      onChange={(e) => setBookData({...bookData, title: e.target.value})}
                      placeholder="例如：React 高级开发指南"
                      className="input-field"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      图书简介 *
                    </label>
                    <textarea
                      value={bookData.description}
                      onChange={(e) => setBookData({...bookData, description: e.target.value})}
                      placeholder="简要描述这本书的主要内容和价值..."
                      rows={4}
                      className="input-field"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      目标读者
                    </label>
                    <input
                      type="text"
                      value={bookData.targetAudience}
                      onChange={(e) => setBookData({...bookData, targetAudience: e.target.value})}
                      placeholder="例如：有一定经验的前端开发者"
                      className="input-field"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      主要目标
                    </label>
                    <textarea
                      value={bookData.mainGoal}
                      onChange={(e) => setBookData({...bookData, mainGoal: e.target.value})}
                      placeholder="读者阅读这本书后能够获得什么知识或技能？"
                      rows={3}
                      className="input-field"
                    />
                  </div>
                </div>
              </motion.div>
            )}

            {currentStep === 2 && (
              <motion.div
                key="step2"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-6"
              >
                <div className="text-center mb-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">
                    选择图书模板
                  </h2>
                  <p className="text-gray-600">
                    选择最适合你内容的结构模板，我们会为你生成相应的章节大纲
                  </p>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  {templates.map((template) => (
                    <div
                      key={template.id}
                      onClick={() => setBookData({...bookData, template})}
                      className={`p-6 rounded-lg border-2 cursor-pointer transition-all ${
                        bookData.template?.id === template.id
                          ? 'border-primary-500 bg-primary-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <div className="flex items-start space-x-4">
                        <div className={`p-3 rounded-lg ${template.bgColor}`}>
                          <template.icon className={`h-6 w-6 ${template.color}`} />
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center justify-between mb-2">
                            <h3 className="text-lg font-semibold text-gray-900">
                              {template.name}
                            </h3>
                            <span className={`px-2 py-1 text-xs font-medium rounded-full ${getDifficultyColor(template.difficulty)}`}>
                              {getDifficultyText(template.difficulty)}
                            </span>
                          </div>
                          <p className="text-gray-600 text-sm mb-4">
                            {template.description}
                          </p>
                          <div className="space-y-2">
                            <div className="flex items-center text-sm text-gray-500">
                              <ClockIcon className="h-4 w-4 mr-1" />
                              预计时间：{template.estimatedTime}
                            </div>
                            <div>
                              <p className="text-sm text-gray-500 mb-1">章节结构：</p>
                              <div className="flex flex-wrap gap-1">
                                {template.chapters.slice(0, 3).map((chapter, index) => (
                                  <span key={index} className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">
                                    {chapter}
                                  </span>
                                ))}
                                {template.chapters.length > 3 && (
                                  <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">
                                    +{template.chapters.length - 3}
                                  </span>
                                )}
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </motion.div>
            )}

            {currentStep === 3 && (
              <motion.div
                key="step3"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-6"
              >
                <div className="text-center mb-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">
                    完善创作细节
                  </h2>
                  <p className="text-gray-600">
                    设置写作风格和关键主题，让 AI 更好地理解你的需求
                  </p>
                </div>

                <div className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-4">
                      写作风格
                    </label>
                    <div className="grid md:grid-cols-2 gap-4">
                      {writingStyles.map((style) => (
                        <div
                          key={style.id}
                          onClick={() => setBookData({...bookData, writingStyle: style.id as any})}
                          className={`p-4 rounded-lg border cursor-pointer transition-all ${
                            bookData.writingStyle === style.id
                              ? 'border-primary-500 bg-primary-50'
                              : 'border-gray-200 hover:border-gray-300'
                          }`}
                        >
                          <h4 className="font-medium text-gray-900 mb-1">{style.name}</h4>
                          <p className="text-sm text-gray-600">{style.description}</p>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      关键主题
                    </label>
                    <p className="text-sm text-gray-500 mb-3">
                      添加你想要重点讲解的主题或技术点
                    </p>
                    <div className="flex flex-wrap gap-2 mb-3">
                      {bookData.keyTopics.map((topic, index) => (
                        <span
                          key={index}
                          className="inline-flex items-center px-3 py-1 bg-primary-100 text-primary-800 text-sm rounded-full"
                        >
                          {topic}
                          <button
                            onClick={() => removeKeyTopic(topic)}
                            className="ml-2 text-primary-600 hover:text-primary-800"
                          >
                            ×
                          </button>
                        </span>
                      ))}
                    </div>
                    <div className="flex space-x-2">
                      <input
                        type="text"
                        placeholder="输入主题并按回车添加"
                        className="flex-1 input-field"
                        onKeyPress={(e) => {
                          if (e.key === 'Enter') {
                            addKeyTopic((e.target as HTMLInputElement).value);
                            (e.target as HTMLInputElement).value = ''
                          }
                        }}
                      />
                    </div>
                  </div>
                </div>
              </motion.div>
            )}

            {currentStep === 4 && (
              <motion.div
                key="step4"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-6"
              >
                <div className="text-center mb-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">
                    确认创建图书
                  </h2>
                  <p className="text-gray-600">
                    检查你的设置，确认无误后开始创作之旅
                  </p>
                </div>

                <div className="bg-gray-50 rounded-lg p-6 space-y-4">
                  <div>
                    <h3 className="font-medium text-gray-900 mb-2">基本信息</h3>
                    <div className="space-y-2 text-sm">
                      <p><span className="text-gray-600">标题：</span>{bookData.title}</p>
                      <p><span className="text-gray-600">简介：</span>{bookData.description}</p>
                      {bookData.targetAudience && (
                        <p><span className="text-gray-600">目标读者：</span>{bookData.targetAudience}</p>
                      )}
                    </div>
                  </div>

                  {bookData.template && (
                    <div>
                      <h3 className="font-medium text-gray-900 mb-2">选择模板</h3>
                      <div className="flex items-center space-x-3">
                        <div className={`p-2 rounded ${bookData.template.bgColor}`}>
                          <bookData.template.icon className={`h-5 w-5 ${bookData.template.color}`} />
                        </div>
                        <div>
                          <p className="font-medium">{bookData.template.name}</p>
                          <p className="text-sm text-gray-600">{bookData.template.description}</p>
                        </div>
                      </div>
                    </div>
                  )}

                  <div>
                    <h3 className="font-medium text-gray-900 mb-2">写作设置</h3>
                    <div className="space-y-2 text-sm">
                      <p>
                        <span className="text-gray-600">写作风格：</span>
                        {writingStyles.find(s => s.id === bookData.writingStyle)?.name}
                      </p>
                      {bookData.keyTopics.length > 0 && (
                        <div>
                          <span className="text-gray-600">关键主题：</span>
                          <div className="flex flex-wrap gap-1 mt-1">
                            {bookData.keyTopics.map((topic, index) => (
                              <span key={index} className="px-2 py-1 bg-primary-100 text-primary-800 text-xs rounded">
                                {topic}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="flex items-start space-x-3">
                    <SparklesIcon className="h-6 w-6 text-blue-600 mt-0.5" />
                    <div>
                      <h4 className="font-medium text-blue-900 mb-1">AI 助手已准备就绪</h4>
                      <p className="text-sm text-blue-700">
                        基于你的设置，AI 助手将为你生成初始大纲，并在创作过程中提供智能建议。
                        你可以随时调整内容结构和写作方向。
                      </p>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* 底部操作按钮 */}
        <div className="flex justify-between items-center mt-8">
          <button
            onClick={handlePrevious}
            disabled={currentStep === 1}
            className="flex items-center space-x-2 px-4 py-2 text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ArrowLeftIcon className="h-5 w-5" />
            <span>上一步</span>
          </button>

          <div className="flex space-x-4">
            <Link href="/dashboard" className="btn-secondary">
              取消
            </Link>
            {currentStep < 4 ? (
              <button
                onClick={handleNext}
                disabled={
                  (currentStep === 1 && (!bookData.title || !bookData.description)) ||
                  (currentStep === 2 && !bookData.template)
                }
                className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span>下一步</span>
                <ArrowRightIcon className="h-5 w-5" />
              </button>
            ) : (
              <button
                onClick={handleCreateBook}
                className="btn-primary flex items-center space-x-2"
              >
                <BookOpenIcon className="h-5 w-5" />
                <span>开始创作</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}