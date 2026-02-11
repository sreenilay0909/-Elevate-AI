
import React from 'react';
import { 
  LayoutDashboard, 
  UserCircle, 
  TrendingUp, 
  Map as RoadmapIcon, 
  Briefcase,
  Settings,
  LogOut,
  ChevronRight
} from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  const menuItems = [
    { id: 'overview', name: 'Overview', icon: LayoutDashboard },
    { id: 'profiles', name: 'Platform Profiles', icon: UserCircle },
    { id: 'market', name: 'Market Insights', icon: TrendingUp },
    { id: 'roadmap', name: 'Growth Roadmap', icon: RoadmapIcon },
    { id: 'jobs', name: 'Job Matching', icon: Briefcase },
  ];

  return (
    <aside className="fixed left-0 top-0 h-full w-64 bg-slate-900 text-slate-300 z-50 transition-all duration-300">
      <div className="p-6">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
            <TrendingUp size={20} className="text-white" />
          </div>
          ElevateAI
        </h1>
      </div>
      
      <nav className="mt-6 px-4 space-y-2">
        {menuItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setActiveTab(item.id)}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
              activeTab === item.id 
                ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/20' 
                : 'hover:bg-slate-800 hover:text-white'
            }`}
          >
            <item.icon size={20} />
            <span className="font-medium">{item.name}</span>
            {activeTab === item.id && <ChevronRight size={16} className="ml-auto" />}
          </button>
        ))}
      </nav>

      <div className="absolute bottom-8 left-0 w-full px-6 border-t border-slate-800 pt-8">
        <button className="flex items-center gap-3 text-slate-400 hover:text-white transition-colors">
          <Settings size={20} />
          <span>Settings</span>
        </button>
        <button className="flex items-center gap-3 text-red-400 hover:text-red-300 transition-colors mt-6">
          <LogOut size={20} />
          <span>Log Out</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
