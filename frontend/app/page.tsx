'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  BookOpenIcon, 
  PencilSquareIcon, 
  SparklesIcon,
  ArrowRightIcon,
  LightBulbIcon,
  DocumentTextIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline'
import Link from 'next/link'

export default function HomePage() {
  const [hoveredFeature, setHoveredFeature] = useState<number | null>(null)
  const [isFirstVisit, setIsFirstVisit] = useState(true)
  
  // 检测是否首次访问
  useEffect(() => {
    const hasVisited = localStorage.getItem('bookagent-visited')
    if (hasVisited) {
      setIsFirstVisit(false)
    } else {
      localStorage.setItem('bookagent-visited', 'true')
    }
  }, [])

  const features = [
    {
      icon: LightBulbIcon,
      title: '思想启发',
      description: '通过AI助手激发创作灵感，将抽象思维转化为具体内容',
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-50',
    },
    {
      icon: PencilSquareIcon,
      title: '智能写作',
      description: '基于大语言模型的智能内容生成，专注技术图书创作',
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
    },
    {
      icon: DocumentTextIcon,
      title: '结构化编辑',
      description: '提供章节管理、版本控制和协作编辑功能',
      color: 'text-green-600',
      bgColor: 'bg-green-50',
    },
    {
      icon: ChartBarIcon,
      title: '可视化图表',
      description: '自动生成技术架构图、流程图等可视化内容',
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* 导航栏 */}
      <nav className="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <BookOpenIcon className="h-8 w-8 text-primary-600" />
              <span className="text-xl font-bold text-gray-900">BookAgent</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/dashboard" className="btn-primary">
                开始创作
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* 主要内容 */}
      <main>
        {/* Hero 区域 */}
        <section className="relative py-20 px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
                {isFirstVisit ? (
                  <>
                    欢迎来到
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-purple-600">
                      思想传递
                    </span>
                    的世界
                  </>
                ) : (
                  <>
                    专注于
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-purple-600">
                      思想传递
                    </span>
                    的创作平台
                  </>
                )}
              </h1>
              <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
                {isFirstVisit ? (
                  <>
                    在这里，你的每一个想法都值得被精心雕琢。
                    BookAgent 让创作变得简单，让思想传递变得高效。
                    <br />
                    <span className="text-primary-600 font-medium">准备好开始你的创作之旅了吗？</span>
                  </>
                ) : (
                  <>
                    BookAgent 是一个智能技术图书生成系统，让你专注于思想表达，
                    而不是格式排版。通过AI助手，将你的想法转化为结构化的专业内容。
                  </>
                )}
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/dashboard" className="btn-primary text-lg px-8 py-3 group">
                  {isFirstVisit ? '开始我的第一本书' : '立即开始创作'}
                  <ArrowRightIcon className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                </Link>
                <Link href="/demo" className="btn-secondary text-lg px-8 py-3">
                  {isFirstVisit ? '先看看怎么用' : '查看演示'}
                </Link>
              </div>
              
              {isFirstVisit && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 1, duration: 0.6 }}
                  className="mt-8 p-4 bg-blue-50 rounded-lg border border-blue-200 max-w-md mx-auto"
                >
                  <div className="flex items-center space-x-2 text-blue-800">
                    <LightBulbIcon className="h-5 w-5" />
                    <span className="font-medium">新手提示</span>
                  </div>
                  <p className="text-sm text-blue-700 mt-1">
                    只需3分钟，就能创建你的第一个智能图书项目
                  </p>
                </motion.div>
              )}
            </motion.div>
          </div>
        </section>

        {/* 特性展示 */}
        <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                为思想传递而设计
              </h2>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                我们相信好的工具应该让创作者专注于内容本身，而不是技术细节
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {features.map((feature, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  onHoverStart={() => setHoveredFeature(index)}
                  onHoverEnd={() => setHoveredFeature(null)}
                  className="relative"
                >
                  <div className={`card hover:shadow-lg transition-all duration-300 ${
                    hoveredFeature === index ? 'transform -translate-y-2' : ''
                  }`}>
                    <div className={`inline-flex p-3 rounded-lg ${feature.bgColor} mb-4`}>
                      <feature.icon className={`h-6 w-6 ${feature.color}`} />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600 text-sm leading-relaxed">
                      {feature.description}
                    </p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* 工作流程 */}
        <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-50">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                简单的创作流程
              </h2>
              <p className="text-lg text-gray-600">
                从想法到成书，只需三个步骤
              </p>
            </div>

            <div className="space-y-12">
              {[
                {
                  step: '01',
                  title: '表达想法',
                  description: '用自然语言描述你的图书主题、目标读者和核心观点',
                  icon: LightBulbIcon,
                },
                {
                  step: '02',
                  title: 'AI 协作',
                  description: 'AI助手帮助你完善大纲、生成内容、优化结构',
                  icon: SparklesIcon,
                },
                {
                  step: '03',
                  title: '精炼成书',
                  description: '通过可视化编辑器调整内容，导出专业格式的图书',
                  icon: BookOpenIcon,
                },
              ].map((item, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.6 }}
                  className={`flex items-center gap-8 ${
                    index % 2 === 1 ? 'flex-row-reverse' : ''
                  }`}
                >
                  <div className="flex-1">
                    <div className="flex items-center gap-4 mb-4">
                      <span className="text-4xl font-bold text-primary-600">
                        {item.step}
                      </span>
                      <h3 className="text-2xl font-semibold text-gray-900">
                        {item.title}
                      </h3>
                    </div>
                    <p className="text-lg text-gray-600 leading-relaxed">
                      {item.description}
                    </p>
                  </div>
                  <div className="flex-shrink-0">
                    <div className="w-24 h-24 bg-primary-100 rounded-full flex items-center justify-center">
                      <item.icon className="h-12 w-12 text-primary-600" />
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA 区域 */}
        <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-primary-600 to-purple-600">
          <div className="max-w-4xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
                开始你的创作之旅
              </h2>
              <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
                让AI成为你的创作伙伴，专注于思想的表达和传递
              </p>
              <Link href="/dashboard" className="inline-flex items-center bg-white text-primary-600 font-semibold px-8 py-3 rounded-lg hover:bg-gray-50 transition-colors">
                立即开始
                <ArrowRightIcon className="ml-2 h-5 w-5" />
              </Link>
            </motion.div>
          </div>
        </section>
      </main>

      {/* 页脚 */}
      <footer className="bg-gray-900 text-white py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <BookOpenIcon className="h-6 w-6" />
              <span className="text-lg font-semibold">BookAgent</span>
            </div>
            <div className="text-gray-400 text-sm">
              © 2024 BookAgent. 专注于思想传递的智能创作平台.
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}