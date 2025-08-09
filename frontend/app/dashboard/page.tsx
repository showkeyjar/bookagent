'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  PlusIcon,
  BookOpenIcon,
  PencilSquareIcon,
  DocumentTextIcon,
  ChartBarIcon,
  SparklesIcon,
  FolderIcon,
  ClockIcon,
  UserIcon,
  Cog6ToothIcon
} from '@heroicons/react/24/outline'
import Link from 'next/link'

interface Book {
  id: string
  title: string
  description: string
  status: 'draft' | 'writing' | 'review' | 'published'
  progress: number
  lastModified: string
  wordCount: number
  chapters: number
}

export default function DashboardPage() {
  const [books, setBooks] = useState<Book[]>([])
  const [selectedView, setSelectedView] = useState<'grid' | 'list'>('grid')
  const [isLoading, setIsLoading] = useState(true)

  // 模拟数据加载
  useEffect(() => {
    setTimeout(() => {
      setBooks([
        {
          id: '1',
          title: 'React 高级开发指南',
          description: '深入探讨React生态系统的高级概念和最佳实践',
          status: 'writing',
          progress: 65,
          lastModified: '2024-01-15',
          wordCount: 25000,
          chapters: 12
        },
        {
          id: '2',
          title: '微服务架构设计模式',
          description: '现代微服务架构的设计原则和实践案例',
          status: 'draft',
          progress: 20,
          lastModified: '2024-01-10',
          wordCount: 8000,
          chapters: 8
        },
        {
          id: '3',
          title: 'AI 驱动的软件开发',
          description: '探索人工智能在软件开发中的应用和未来趋势',
          status: 'review',
          progress: 90,
          lastModified: '2024-01-12',
          wordCount: 45000,
          chapters: 15
        }
      ])
      setIsLoading(false)
    }, 1000)
  }, [])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'draft': return 'bg-gray-100 text-gray-800'
      case 'writing': return 'bg-blue-100 text-blue-800'
      case 'review': return 'bg-yellow-100 text-yellow-800'
      case 'published': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case 'draft': return '草稿'
      case 'writing': return '写作中'
      case 'review': return '审阅中'
      case 'published': return '已发布'
      default: return '未知'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 顶部导航 */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <Link href="/" className="flex items-center space-x-2">
                <BookOpenIcon className="h-8 w-8 text-primary-600" />
                <span className="text-xl font-bold text-gray-900">BookAgent</span>
              </Link>
              <div className="hidden md:flex items-center space-x-1">
                <button className="px-3 py-2 text-sm font-medium text-primary-600 bg-primary-50 rounded-md">
                  我的图书
                </button>
                <button className="px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 rounded-md">
                  模板库
                </button>
                <button className="px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 rounded-md">
                  协作空间
                </button>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <button className="p-2 text-gray-400 hover:text-gray-600">
                <Cog6ToothIcon className="h-5 w-5" />
              </button>
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
                  <UserIcon className="h-5 w-5 text-white" />
                </div>
                <span className="text-sm font-medium text-gray-700">创作者</span>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 页面标题和操作 */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">我的图书</h1>
            <p className="text-gray-600">管理你的创作项目，专注于思想的表达</p>
          </div>
          <div className="flex items-center space-x-4 mt-4 sm:mt-0">
            <Link 
              href="/create" 
              className="btn-primary flex items-center space-x-2"
            >
              <PlusIcon className="h-5 w-5" />
              <span>新建图书</span>
            </Link>
          </div>
        </div>

        {/* 快速统计 */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {[
            { label: '总图书数', value: books.length, icon: BookOpenIcon, color: 'text-blue-600' },
            { label: '进行中', value: books.filter(b => b.status === 'writing').length, icon: PencilSquareIcon, color: 'text-green-600' },
            { label: '总字数', value: books.reduce((sum, b) => sum + b.wordCount, 0).toLocaleString(), icon: DocumentTextIcon, color: 'text-purple-600' },
            { label: '本月更新', value: '12', icon: ClockIcon, color: 'text-orange-600' },
          ].map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="card"
            >
              <div className="flex items-center">
                <div className={`p-2 rounded-lg bg-gray-50 mr-4`}>
                  <stat.icon className={`h-6 w-6 ${stat.color}`} />
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                  <p className="text-sm text-gray-600">{stat.label}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* 图书列表 */}
        <div className="card">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-gray-900">最近的项目</h2>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setSelectedView('grid')}
                className={`p-2 rounded-md ${selectedView === 'grid' ? 'bg-primary-100 text-primary-600' : 'text-gray-400 hover:text-gray-600'}`}
              >
                <ChartBarIcon className="h-5 w-5" />
              </button>
              <button
                onClick={() => setSelectedView('list')}
                className={`p-2 rounded-md ${selectedView === 'list' ? 'bg-primary-100 text-primary-600' : 'text-gray-400 hover:text-gray-600'}`}
              >
                <FolderIcon className="h-5 w-5" />
              </button>
            </div>
          </div>

          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
              <span className="ml-2 text-gray-600">加载中...</span>
            </div>
          ) : (
            <AnimatePresence mode="wait">
              {selectedView === 'grid' ? (
                <motion.div
                  key="grid"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
                >
                  {books.map((book, index) => (
                    <motion.div
                      key={book.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: index * 0.1 }}
                      className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer group"
                    >
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex-1">
                          <h3 className="text-lg font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">
                            {book.title}
                          </h3>
                          <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                            {book.description}
                          </p>
                        </div>
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(book.status)}`}>
                          {getStatusText(book.status)}
                        </span>
                      </div>
                      
                      <div className="space-y-3">
                        <div>
                          <div className="flex justify-between text-sm text-gray-600 mb-1">
                            <span>进度</span>
                            <span>{book.progress}%</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                              style={{ width: `${book.progress}%` }}
                            ></div>
                          </div>
                        </div>
                        
                        <div className="flex justify-between text-sm text-gray-600">
                          <span>{book.wordCount.toLocaleString()} 字</span>
                          <span>{book.chapters} 章节</span>
                        </div>
                        
                        <div className="flex justify-between items-center pt-2 border-t border-gray-100">
                          <span className="text-xs text-gray-500">
                            {book.lastModified}
                          </span>
                          <Link 
                            href={`/editor/${book.id}`}
                            className="text-primary-600 hover:text-primary-700 text-sm font-medium"
                          >
                            继续编辑
                          </Link>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </motion.div>
              ) : (
                <motion.div
                  key="list"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="space-y-4"
                >
                  {books.map((book, index) => (
                    <motion.div
                      key={book.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.5, delay: index * 0.1 }}
                      className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer"
                    >
                      <div className="flex items-center space-x-4 flex-1">
                        <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                          <BookOpenIcon className="h-6 w-6 text-primary-600" />
                        </div>
                        <div className="flex-1">
                          <h3 className="text-lg font-medium text-gray-900">{book.title}</h3>
                          <p className="text-sm text-gray-600">{book.description}</p>
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-6">
                        <div className="text-center">
                          <p className="text-sm font-medium text-gray-900">{book.progress}%</p>
                          <p className="text-xs text-gray-500">进度</p>
                        </div>
                        <div className="text-center">
                          <p className="text-sm font-medium text-gray-900">{book.wordCount.toLocaleString()}</p>
                          <p className="text-xs text-gray-500">字数</p>
                        </div>
                        <div className="text-center">
                          <p className="text-sm font-medium text-gray-900">{book.chapters}</p>
                          <p className="text-xs text-gray-500">章节</p>
                        </div>
                        <span className={`px-3 py-1 text-xs font-medium rounded-full ${getStatusColor(book.status)}`}>
                          {getStatusText(book.status)}
                        </span>
                        <Link 
                          href={`/editor/${book.id}`}
                          className="btn-primary text-sm"
                        >
                          编辑
                        </Link>
                      </div>
                    </motion.div>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          )}
        </div>

        {/* 快速操作 */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link href="/create" className="card hover:shadow-md transition-shadow cursor-pointer group">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center group-hover:bg-blue-200 transition-colors">
                <PlusIcon className="h-6 w-6 text-blue-600" />
              </div>
              <div>
                <h3 className="text-lg font-medium text-gray-900">创建新图书</h3>
                <p className="text-sm text-gray-600">从零开始你的创作之旅</p>
              </div>
            </div>
          </Link>
          
          <Link href="/templates" className="card hover:shadow-md transition-shadow cursor-pointer group">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center group-hover:bg-purple-200 transition-colors">
                <DocumentTextIcon className="h-6 w-6 text-purple-600" />
              </div>
              <div>
                <h3 className="text-lg font-medium text-gray-900">浏览模板</h3>
                <p className="text-sm text-gray-600">使用预设模板快速开始</p>
              </div>
            </div>
          </Link>
          
          <Link href="/ai-assistant" className="card hover:shadow-md transition-shadow cursor-pointer group">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center group-hover:bg-yellow-200 transition-colors">
                <SparklesIcon className="h-6 w-6 text-yellow-600" />
              </div>
              <div>
                <h3 className="text-lg font-medium text-gray-900">AI 助手</h3>
                <p className="text-sm text-gray-600">获取创作灵感和建议</p>
              </div>
            </div>
          </Link>
        </div>
      </div>
    </div>
  )
}