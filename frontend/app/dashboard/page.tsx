'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { portfolioAPI, assetsAPI, transactionsAPI } from '@/lib/api';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip, LineChart, Line, XAxis, YAxis, CartesianGrid } from 'recharts';
import TransactionDetailModal from '@/components/TransactionDetailModal';

const COLORS = ['#0f172a', '#1e40af', '#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe'];
const TAB_COLORS = {
  'stock-etf': '#3b82f6',
  'cic': '#8b5cf6',
  'foundation': '#10b981',
  'crypto': '#f59e0b',
  'currency-metal': '#ec4899',
  'other': '#6b7280',
};

// Helper function to get current local time in datetime-local format
const getLocalDateTime = () => {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  return `${year}-${month}-${day}T${hours}:${minutes}`;
};

// Helper function to format currency
const formatCurrency = (value: number, currencyCode: string = 'USD'): string => {
  const currencySymbols: { [key: string]: string } = {
    USD: '$',
    EUR: '€',
    GBP: '£',
    JPY: '¥',
    CAD: 'C$',
    AUD: 'A$',
    HKD: 'HK$',
    CNY: '¥',
  };
  return `${currencySymbols[currencyCode] || '$'}${value.toFixed(2)}`;
};

// Help Tooltip Component
const HelpTooltip = ({ content }: { content: string }) => {
  const [show, setShow] = useState(false);

  return (
    <div className="relative inline-block ml-2">
      <button
        type="button"
        onMouseEnter={() => setShow(true)}
        onMouseLeave={() => setShow(false)}
        onClick={() => setShow(!show)}
        className="w-5 h-5 rounded-full bg-slate-200 hover:bg-slate-300 text-slate-600 hover:text-slate-800 flex items-center justify-center text-xs font-bold transition-all"
      >
        ?
      </button>
      {show && (
        <div className="absolute z-50 left-0 top-6 w-64 p-3 bg-slate-800 text-white text-xs rounded-lg shadow-lg">
          <div className="absolute -top-1 left-2 w-2 h-2 bg-slate-800 transform rotate-45"></div>
          {content}
        </div>
      )}
    </div>
  );
};

type TabType = 'overall' | 'stock-etf' | 'cic' | 'foundation' | 'crypto' | 'currency-metal' | 'other';

interface CategoryData {
  name: string;
  currencies: {
    [key: string]: {
      assets: any[];
      total_value: number;
      total_invested: number;
      total_profit_loss: number;
    };
  };
  total_value: number;
  total_invested: number;
  total_profit_loss: number;
}

interface PortfolioData {
  portfolio_summary: {
    total_value: number;
    total_invested: number;
    total_profit_loss: number;
    total_profit_loss_percentage: number;
    assets_count: number;
  };
  categories: {
    [key: string]: CategoryData;
  };
}

export default function DashboardPage() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<TabType>('overall');
  const [portfolioData, setPortfolioData] = useState<PortfolioData | null>(null);
  const [performanceData, setPerformanceData] = useState<any>(null);
  const [transactions, setTransactions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddAsset, setShowAddAsset] = useState(false);
  const [showEditAsset, setShowEditAsset] = useState(false);
  const [editingAsset, setEditingAsset] = useState<any>(null);
  const [showAddTransaction, setShowAddTransaction] = useState(false);
  const [selectedTransactionId, setSelectedTransactionId] = useState<number | null>(null);
  const [performancePeriod, setPerformancePeriod] = useState<1 | 5 | 7 | 30 | 90 | 365>(30);
  const [stockSearchResults, setStockSearchResults] = useState<any[]>([]);
  const [searchLoading, setSearchLoading] = useState(false);
  const [showSearchResults, setShowSearchResults] = useState(false);
  const [autoFillData, setAutoFillData] = useState<any>(null);
  const [currencyFilter, setCurrencyFilter] = useState<string>('all');
  const [sortField, setSortField] = useState<string>('symbol');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc');
  const [assetForm, setAssetForm] = useState({
    symbol: '',
    name: '',
    quantity: 0,
    average_buy_price: 0,
    asset_type: 'stock',
    asset_category: 'stock-etf',
    currency: 'USD',
    purchase_date: getLocalDateTime(),
    remarks: '',
  });
  const [transactionForm, setTransactionForm] = useState({
    asset_id: 0,
    transaction_type: 'buy' as 'buy' | 'sell',
    quantity: 0,
    price_per_unit: 0,
    notes: '',
    transaction_date: getLocalDateTime(),
  });

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }
    fetchData();
  }, [router, performancePeriod]);

  const fetchData = async () => {
    try {
      const [portfolioRes, transactionsRes, performanceRes] = await Promise.all([
        portfolioAPI.getByCategory(),
        transactionsAPI.getAll(0, 10),
        portfolioAPI.getPerformanceHistory(performancePeriod),
      ]);
      setPortfolioData(portfolioRes.data);
      setTransactions(transactionsRes.data);
      setPerformanceData(performanceRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
      localStorage.removeItem('token');
      router.push('/login');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    router.push('/login');
  };

  const handleSymbolChange = async (value: string) => {
    const upperValue = value.toUpperCase();
    setAssetForm({ ...assetForm, symbol: upperValue });

    if (upperValue.length > 0) {
      try {
        const response = await assetsAPI.getAutoFillData(upperValue);
        if (response.data) {
          setAutoFillData(response.data);
          // Auto-apply immediately
          setAssetForm({
            ...assetForm,
            symbol: upperValue,
            name: response.data.name,
            asset_type: response.data.asset_type,
            asset_category: response.data.asset_category,
            currency: response.data.currency,
          });
        }
      } catch (error) {
        // Symbol not found in database, clear auto-fill
        setAutoFillData(null);
      }
    } else {
      setAutoFillData(null);
    }
  };

  const handleApplyAutoFill = () => {
    if (autoFillData) {
      setAssetForm({
        ...assetForm,
        name: autoFillData.name,
        asset_type: autoFillData.asset_type,
        asset_category: autoFillData.asset_category,
        currency: autoFillData.currency,
      });
      setAutoFillData(null);
    }
  };

  const handleAddAsset = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validate form
    if (!assetForm.symbol || !assetForm.name) {
      alert('Please fill in Symbol and Name');
      return;
    }

    if (assetForm.quantity <= 0 || assetForm.average_buy_price <= 0) {
      alert('Quantity and Average Buy Price must be greater than 0');
      return;
    }

    try {
      console.log('Submitting asset:', assetForm);
      const response = await assetsAPI.create(assetForm);
      console.log('Asset created:', response.data);

      setShowAddAsset(false);
      setAssetForm({
        symbol: '',
        name: '',
        quantity: 0,
        average_buy_price: 0,
        asset_type: 'stock',
        asset_category: 'stock-etf',
        currency: 'USD',
        purchase_date: getLocalDateTime(),
        remarks: '',
      });
      setAutoFillData(null);

      // Refresh data
      await fetchData();

      alert('Asset added successfully!');
    } catch (error: any) {
      console.error('Error adding asset:', error);
      const errorMsg = error.response?.data?.detail || error.message || 'Error adding asset';
      alert(errorMsg);
    }
  };

  const handleAddTransaction = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await transactionsAPI.create(transactionForm);
      setShowAddTransaction(false);
      setTransactionForm({
        asset_id: 0,
        transaction_type: 'buy',
        quantity: 0,
        price_per_unit: 0,
        notes: '',
        transaction_date: getLocalDateTime(),
      });
      fetchData();
      alert('Transaction added successfully!');
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Error adding transaction');
    }
  };

  const handleEditAsset = (asset: any) => {
    setEditingAsset(asset);
    setAssetForm({
      symbol: asset.symbol,
      name: asset.name,
      quantity: asset.quantity,
      average_buy_price: asset.average_buy_price,
      asset_type: asset.asset_type,
      asset_category: asset.asset_category,
      currency: asset.currency,
      purchase_date: asset.purchase_date || getLocalDateTime(),
      remarks: asset.remarks || '',
    });
    setShowEditAsset(true);
  };

  const handleUpdateAsset = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!assetForm.symbol || !assetForm.name) {
      alert('Please fill in Symbol and Name');
      return;
    }

    if (assetForm.quantity <= 0 || assetForm.average_buy_price <= 0) {
      alert('Quantity and Average Buy Price must be greater than 0');
      return;
    }

    try {
      await assetsAPI.update(editingAsset.id, assetForm);
      setShowEditAsset(false);
      setEditingAsset(null);
      setAssetForm({
        symbol: '',
        name: '',
        quantity: 0,
        average_buy_price: 0,
        asset_type: 'stock',
        asset_category: 'stock-etf',
        currency: 'USD',
        purchase_date: getLocalDateTime(),
        remarks: '',
      });
      await fetchData();
      alert('Asset updated successfully!');
    } catch (error: any) {
      console.error('Error updating asset:', error);
      const errorMsg = error.response?.data?.detail || error.message || 'Error updating asset';
      alert(errorMsg);
    }
  };

  const handleDeleteAsset = async (assetId: number) => {
    if (!confirm('Are you sure you want to delete this asset? This action cannot be undone.')) {
      return;
    }

    try {
      await assetsAPI.delete(assetId);
      await fetchData();
      alert('Asset deleted successfully!');
    } catch (error: any) {
      console.error('Error deleting asset:', error);
      const errorMsg = error.response?.data?.detail || error.message || 'Error deleting asset';
      alert(errorMsg);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="text-center">
          <div className="inline-block w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
          <p className="mt-4 text-slate-600 font-medium">Loading your portfolio...</p>
        </div>
      </div>
    );
  }

  const summary = portfolioData?.portfolio_summary || {
    total_invested: 0,
    assets_count: 0,
  };

  // Calculate per-currency totals from all categories
  const currencyTotals: { [key: string]: { invested: number } } = {};

  if (portfolioData?.categories) {
    Object.values(portfolioData.categories).forEach((category: any) => {
      if (category.currencies) {
        Object.entries(category.currencies).forEach(([currency, data]: [string, any]) => {
          if (!currencyTotals[currency]) {
            currencyTotals[currency] = { invested: 0 };
          }
          currencyTotals[currency].invested += data.total_invested || 0;
        });
      }
    });
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-slate-100 to-slate-200">
      {/* Navigation */}
      <nav className="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-slate-900 to-slate-700 flex items-center justify-center shadow-lg">
                <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
              <div>
                <h1 className="text-xl font-bold text-slate-900">Portfolio Manager</h1>
                <p className="text-xs text-slate-500">Professional Investment Dashboard</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={() => router.push('/transactions')}
                className="px-4 py-2 text-slate-700 hover:text-slate-900 font-medium transition-colors"
              >
                Transactions
              </button>
              <button
                onClick={() => router.push('/profile')}
                className="px-4 py-2 text-slate-700 hover:text-slate-900 font-medium transition-colors"
              >
                Profile
              </button>
              <button
                onClick={handleLogout}
                className="px-4 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 font-medium transition-all"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Portfolio Summary Cards - Per Currency */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* Total Invested by Currency */}
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center">
                <p className="text-sm font-semibold text-slate-700">Total Invested</p>
                <HelpTooltip content="Total amount of capital you have invested in each currency. This is the sum of all your purchase prices." />
              </div>
              <div className="w-10 h-10 rounded-lg bg-slate-50 flex items-center justify-center">
                <svg className="w-5 h-5 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                </svg>
              </div>
            </div>
            <div className="space-y-2">
              {Object.entries(currencyTotals).map(([currency, data]) => (
                <div key={currency} className="flex justify-between items-center">
                  <span className="text-xs font-medium text-slate-600">{currency}</span>
                  <span className="text-lg font-bold text-slate-900">{formatCurrency(data.invested, currency)}</span>
                </div>
              ))}
              {Object.keys(currencyTotals).length === 0 && (
                <p className="text-sm text-slate-400 italic">No investments yet</p>
              )}
            </div>
          </div>

          {/* Total Assets Count Card */}
          <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl shadow-sm border border-purple-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-semibold text-slate-700 mb-1">Total Assets</p>
                <p className="text-4xl font-bold text-slate-900">{summary.assets_count}</p>
                <p className="text-xs text-slate-500 mt-1">Assets in portfolio</p>
              </div>
              <div className="w-16 h-16 rounded-xl bg-purple-100 flex items-center justify-center">
                <svg className="w-8 h-8 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 mb-8 overflow-hidden">
          <div className="flex flex-wrap border-b border-slate-200 overflow-x-auto">
            <button
              onClick={() => setActiveTab('overall')}
              className={`px-4 py-3 font-medium text-sm transition-all whitespace-nowrap ${
                activeTab === 'overall'
                  ? 'border-b-2 border-blue-600 text-blue-600 bg-blue-50'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Overview
            </button>
            <button
              onClick={() => setActiveTab('stock-etf')}
              className={`px-4 py-3 font-medium text-sm transition-all whitespace-nowrap ${
                activeTab === 'stock-etf'
                  ? 'border-b-2 border-blue-600 text-blue-600 bg-blue-50'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Stock & ETF
            </button>
            <button
              onClick={() => setActiveTab('cic')}
              className={`px-4 py-3 font-medium text-sm transition-all whitespace-nowrap ${
                activeTab === 'cic'
                  ? 'border-b-2 border-purple-600 text-purple-600 bg-purple-50'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              CIC
            </button>
            <button
              onClick={() => setActiveTab('foundation')}
              className={`px-4 py-3 font-medium text-sm transition-all whitespace-nowrap ${
                activeTab === 'foundation'
                  ? 'border-b-2 border-green-600 text-green-600 bg-green-50'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Foundation
            </button>
            <button
              onClick={() => setActiveTab('crypto')}
              className={`px-4 py-3 font-medium text-sm transition-all whitespace-nowrap ${
                activeTab === 'crypto'
                  ? 'border-b-2 border-amber-600 text-amber-600 bg-amber-50'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Crypto
            </button>
            <button
              onClick={() => setActiveTab('currency-metal')}
              className={`px-4 py-3 font-medium text-sm transition-all whitespace-nowrap ${
                activeTab === 'currency-metal'
                  ? 'border-b-2 border-pink-600 text-pink-600 bg-pink-50'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Currency & Metals
            </button>
            <button
              onClick={() => setActiveTab('other')}
              className={`px-4 py-3 font-medium text-sm transition-all whitespace-nowrap ${
                activeTab === 'other'
                  ? 'border-b-2 border-gray-600 text-gray-600 bg-gray-50'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Other
            </button>
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {activeTab === 'overall' && (
              <div className="space-y-6">
                <div className="flex justify-between items-center mb-4">
                  <div className="flex items-center">
                    <h2 className="text-xl font-bold text-slate-900">Overall Portfolio</h2>
                    <HelpTooltip content="Overview of all your investment categories. Click on individual tabs above to see detailed breakdowns by Stock & ETF, CIC, Foundation, Crypto, Currency & Metals, or Other." />
                  </div>
                  <button
                    onClick={() => setShowAddAsset(true)}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition-all"
                  >
                    + Add Asset
                  </button>
                </div>

                {/* Charts Section */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                  {/* Pie Chart - Investment Distribution */}
                  <div className="bg-white rounded-lg p-6 border border-slate-200">
                    <h3 className="text-lg font-semibold text-slate-900 mb-4">Investment Distribution</h3>
                    {Object.values(portfolioData?.categories || {}).some((cat: any) => cat.total_invested > 0) ? (
                      <ResponsiveContainer width="100%" height={300}>
                        <PieChart>
                          <Pie
                            data={Object.entries(portfolioData?.categories || {})
                              .filter(([_, category]: [string, any]) => category.total_invested > 0)
                              .map(([key, category]: [string, any]) => ({
                                name: category.name,
                                value: category.total_invested,
                                color: TAB_COLORS[key as keyof typeof TAB_COLORS] || '#6b7280'
                              }))}
                            cx="50%"
                            cy="50%"
                            labelLine={false}
                            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                            outerRadius={80}
                            fill="#8884d8"
                            dataKey="value"
                          >
                            {Object.entries(portfolioData?.categories || {})
                              .filter(([_, category]: [string, any]) => category.total_invested > 0)
                              .map(([key, _], index) => (
                                <Cell key={`cell-${index}`} fill={TAB_COLORS[key as keyof typeof TAB_COLORS] || '#6b7280'} />
                              ))}
                          </Pie>
                          <Tooltip formatter={(value: number) => `$${value.toFixed(2)}`} />
                          <Legend />
                        </PieChart>
                      </ResponsiveContainer>
                    ) : (
                      <div className="h-[300px] flex items-center justify-center text-slate-400">
                        No investment data available
                      </div>
                    )}
                  </div>

                  {/* Line Chart - Performance History */}
                  <div className="bg-white rounded-lg p-6 border border-slate-200">
                    <div className="flex justify-between items-center mb-4">
                      <h3 className="text-lg font-semibold text-slate-900">Performance History</h3>
                      <select
                        value={performancePeriod}
                        onChange={(e) => setPerformancePeriod(Number(e.target.value) as 1 | 5 | 7 | 30 | 90 | 365)}
                        className="px-3 py-1 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500"
                      >
                        <option value={1}>1 Day</option>
                        <option value={5}>5 Days</option>
                        <option value={7}>1 Week</option>
                        <option value={30}>1 Month</option>
                        <option value={90}>3 Months</option>
                        <option value={365}>1 Year</option>
                      </select>
                    </div>
                    {performanceData && performanceData.length > 0 ? (
                      <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={performanceData}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis
                            dataKey="date"
                            tick={{ fontSize: 12 }}
                            tickFormatter={(value) => {
                              const date = new Date(value);
                              return `${date.getMonth() + 1}/${date.getDate()}`;
                            }}
                          />
                          <YAxis tick={{ fontSize: 12 }} />
                          <Tooltip
                            formatter={(value: number) => `$${value.toFixed(2)}`}
                            labelFormatter={(label) => new Date(label).toLocaleDateString()}
                          />
                          <Legend />
                          <Line type="monotone" dataKey="total_value" stroke="#3b82f6" name="Total Value" strokeWidth={2} />
                        </LineChart>
                      </ResponsiveContainer>
                    ) : (
                      <div className="h-[300px] flex items-center justify-center text-slate-400">
                        No performance data available
                      </div>
                    )}
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {Object.entries(portfolioData?.categories || {}).map(([key, category]: [string, any]) => (
                    category.total_invested > 0 && (
                      <div key={key} className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                        <h3 className="font-semibold text-slate-900 mb-3">{category.name}</h3>
                        <div className="space-y-2 text-sm">
                          {Object.entries(category.currencies || {}).map(([currency, data]: [string, any]) => (
                            <div key={currency} className="flex justify-between">
                              <span className="text-slate-600">{currency}:</span>
                              <span className="font-semibold text-slate-900">{formatCurrency(data.total_invested, currency)}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )
                  ))}
                </div>
              </div>
            )}

            {activeTab !== 'overall' && portfolioData?.categories[activeTab] && (
              <div className="space-y-6">
                <div className="flex justify-between items-center mb-4">
                  <div className="flex items-center">
                    <h2 className="text-xl font-bold text-slate-900">{portfolioData.categories[activeTab].name}</h2>
                    <HelpTooltip content="View all assets in this category. Use the currency filter to show specific currencies, or click column headers to sort. Each asset shows its quantity, average price, current value, and profit/loss." />
                  </div>
                  <button
                    onClick={() => setShowAddAsset(true)}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition-all"
                  >
                    + Add Asset
                  </button>
                </div>

                {/* Currency Filter */}
                <div className="flex items-center gap-4 mb-4">
                  <div className="flex items-center">
                    <label className="text-sm font-semibold text-slate-700">Filter by Currency:</label>
                    <HelpTooltip content="Filter assets by currency. Select 'All Currencies' to see everything, or choose a specific currency (USD, HKD, CNY, etc.) to view only those assets." />
                  </div>
                  <select
                    value={currencyFilter}
                    onChange={(e) => setCurrencyFilter(e.target.value)}
                    className="px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="all">All Currencies</option>
                    {Object.keys(portfolioData.categories[activeTab].currencies || {}).map((currency) => (
                      <option key={currency} value={currency}>{currency}</option>
                    ))}
                  </select>
                </div>

                {/* Summary Stats */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                  <div className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                    <p className="text-sm text-slate-600 mb-1">Total Invested</p>
                    <p className="text-2xl font-bold text-slate-900">${portfolioData.categories[activeTab].total_invested.toFixed(2)}</p>
                  </div>
                  <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                    <p className="text-sm text-slate-600 mb-1">Assets Count</p>
                    <p className="text-2xl font-bold text-blue-600">
                      {Object.values(portfolioData.categories[activeTab].currencies || {}).reduce((sum: number, curr: any) => sum + curr.assets.length, 0)}
                    </p>
                  </div>
                </div>

                {/* Assets Table */}
                <div className="bg-white rounded-lg border border-slate-200 overflow-hidden">
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead className="bg-slate-50">
                        <tr className="border-b border-slate-200">
                          <th
                            className="text-left py-3 px-4 font-semibold text-slate-700 cursor-pointer hover:bg-slate-100"
                            onClick={() => {
                              if (sortField === 'symbol') {
                                setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
                              } else {
                                setSortField('symbol');
                                setSortDirection('asc');
                              }
                            }}
                          >
                            Symbol {sortField === 'symbol' && (sortDirection === 'asc' ? '↑' : '↓')}
                          </th>
                          <th className="text-left py-3 px-4 font-semibold text-slate-700">Name</th>
                          <th
                            className="text-center py-3 px-4 font-semibold text-slate-700 cursor-pointer hover:bg-slate-100"
                            onClick={() => {
                              if (sortField === 'currency') {
                                setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
                              } else {
                                setSortField('currency');
                                setSortDirection('asc');
                              }
                            }}
                          >
                            Currency {sortField === 'currency' && (sortDirection === 'asc' ? '↑' : '↓')}
                          </th>
                          <th className="text-right py-3 px-4 font-semibold text-slate-700">Quantity</th>
                          <th className="text-right py-3 px-4 font-semibold text-slate-700">Avg Price</th>
                          <th className="text-right py-3 px-4 font-semibold text-slate-700">Invested Value</th>
                          <th className="text-center py-3 px-4 font-semibold text-slate-700">Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {(() => {
                          // Collect all assets from all currencies
                          let allAssets: any[] = [];
                          Object.entries(portfolioData.categories[activeTab].currencies || {}).forEach(([currency, data]: [string, any]) => {
                            if (currencyFilter === 'all' || currencyFilter === currency) {
                              allAssets = allAssets.concat(data.assets.map((asset: any) => ({ ...asset, currency })));
                            }
                          });

                          // Sort assets
                          allAssets.sort((a, b) => {
                            let aVal = a[sortField];
                            let bVal = b[sortField];

                            if (typeof aVal === 'string') {
                              aVal = aVal.toLowerCase();
                              bVal = bVal.toLowerCase();
                            }

                            if (sortDirection === 'asc') {
                              return aVal > bVal ? 1 : -1;
                            } else {
                              return aVal < bVal ? 1 : -1;
                            }
                          });

                          return allAssets.length > 0 ? allAssets.map((asset: any) => (
                            <tr key={asset.id} className="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                              <td className="py-3 px-4 font-semibold text-slate-900">{asset.symbol}</td>
                              <td className="py-3 px-4 text-slate-600">{asset.name}</td>
                              <td className="text-center py-3 px-4">
                                <span className="inline-block px-2 py-1 bg-slate-100 text-slate-700 rounded text-xs font-semibold">
                                  {asset.currency}
                                </span>
                              </td>
                              <td className="text-right py-3 px-4 text-slate-900">{asset.quantity.toFixed(2)}</td>
                              <td className="text-right py-3 px-4 text-slate-900">{formatCurrency(asset.average_buy_price, asset.currency)}</td>
                              <td className="text-right py-3 px-4 font-semibold text-slate-900">{formatCurrency(asset.invested_value, asset.currency)}</td>
                              <td className="text-center py-3 px-4">
                                <div className="flex items-center justify-center gap-2">
                                  <button
                                    onClick={() => handleEditAsset(asset)}
                                    className="px-3 py-1 bg-blue-100 text-blue-700 rounded hover:bg-blue-200 text-xs font-medium transition-all"
                                  >
                                    Edit
                                  </button>
                                  <button
                                    onClick={() => handleDeleteAsset(asset.id)}
                                    className="px-3 py-1 bg-red-100 text-red-700 rounded hover:bg-red-200 text-xs font-medium transition-all"
                                  >
                                    Delete
                                  </button>
                                  <button
                                    onClick={() => {
                                      setTransactionForm({ ...transactionForm, asset_id: asset.id });
                                      setShowAddTransaction(true);
                                    }}
                                    className="px-3 py-1 bg-green-100 text-green-700 rounded hover:bg-green-200 text-xs font-medium transition-all"
                                  >
                                    Transaction
                                  </button>
                                </div>
                              </td>
                            </tr>
                          )) : (
                            <tr>
                              <td colSpan={7} className="py-8 text-center text-slate-400 italic">
                                No assets in this category yet
                              </td>
                            </tr>
                          );
                        })()}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Add Asset Modal */}
        {showAddAsset && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-xl shadow-lg max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
              <div className="flex justify-between items-center p-6 border-b border-slate-200 sticky top-0 bg-white">
                <h2 className="text-xl font-bold text-slate-900">Add New Asset</h2>
                <button
                  onClick={() => {
                    setShowAddAsset(false);
                    setAutoFillData(null);
                  }}
                  className="text-slate-500 hover:text-slate-700"
                >
                  ✕
                </button>
              </div>

              <form onSubmit={handleAddAsset} className="p-6 space-y-4">
                {/* Symbol with Auto-fill */}
                <div className="relative">
                  <div className="flex items-center mb-2">
                    <label className="block text-sm font-medium text-slate-700">
                      Symbol *
                      <span className="text-xs text-slate-500 ml-2">(Auto-fills Name, Type, Currency)</span>
                    </label>
                    <HelpTooltip content="Enter the ticker symbol (e.g., AAPL for Apple, 0700 for Tencent, 600519 for Moutai, XAU for Gold, BTC for Bitcoin). The system will automatically fill in the name, type, and currency if the symbol is in our database." />
                  </div>
                  <input
                    type="text"
                    value={assetForm.symbol}
                    onChange={(e) => handleSymbolChange(e.target.value)}
                    placeholder="e.g., AAPL, 0700, 600519, XAU, BTC"
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 uppercase"
                    required
                  />
                  {autoFillData && (
                    <div className="mt-2 p-3 bg-green-50 rounded-lg border border-green-200">
                      <div className="flex items-center gap-2">
                        <svg className="w-5 h-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        <p className="text-sm font-semibold text-green-900">Auto-filled!</p>
                      </div>
                      <p className="text-sm text-slate-700 mt-1">
                        <strong>{autoFillData.name}</strong> • {autoFillData.currency} • {autoFillData.asset_type}
                      </p>
                    </div>
                  )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <div className="flex items-center mb-2">
                      <label className="block text-sm font-medium text-slate-700">Name *</label>
                      <HelpTooltip content="Full name of the asset (e.g., Apple Inc., Tencent Holdings Ltd). This is auto-filled if the symbol is recognized." />
                    </div>
                    <input
                      type="text"
                      value={assetForm.name}
                      onChange={(e) => setAssetForm({ ...assetForm, name: e.target.value })}
                      placeholder="e.g., Apple Inc."
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>

                  <div>
                    <div className="flex items-center mb-2">
                      <label className="block text-sm font-medium text-slate-700">Currency *</label>
                      <HelpTooltip content="The currency this asset is traded in. USD for US stocks, HKD for Hong Kong stocks, CNY for China A-shares, etc. Auto-filled based on symbol." />
                    </div>
                    <select
                      value={assetForm.currency}
                      onChange={(e) => setAssetForm({ ...assetForm, currency: e.target.value })}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="USD">USD ($)</option>
                      <option value="EUR">EUR (€)</option>
                      <option value="GBP">GBP (£)</option>
                      <option value="JPY">JPY (¥)</option>
                      <option value="CAD">CAD (C$)</option>
                      <option value="AUD">AUD (A$)</option>
                      <option value="HKD">HKD (HK$)</option>
                      <option value="CNY">CNY (¥)</option>
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <div className="flex items-center mb-2">
                      <label className="block text-sm font-medium text-slate-700">Quantity *</label>
                      <HelpTooltip content="Number of shares/units you own. Can be decimal (e.g., 10.5 shares). For crypto, enter the amount (e.g., 0.5 BTC)." />
                    </div>
                    <input
                      type="number"
                      step="0.01"
                      value={assetForm.quantity}
                      onChange={(e) => setAssetForm({ ...assetForm, quantity: parseFloat(e.target.value) || 0 })}
                      placeholder="0.00"
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>

                  <div>
                    <div className="flex items-center mb-2">
                      <label className="block text-sm font-medium text-slate-700">Average Buy Price *</label>
                      <HelpTooltip content="The average price you paid per unit/share. If you bought at different prices, calculate the average. This is used to calculate your profit/loss." />
                    </div>
                    <input
                      type="number"
                      step="0.01"
                      value={assetForm.average_buy_price}
                      onChange={(e) => setAssetForm({ ...assetForm, average_buy_price: parseFloat(e.target.value) || 0 })}
                      placeholder="0.00"
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <div className="flex items-center mb-2">
                      <label className="block text-sm font-medium text-slate-700">Asset Type *</label>
                      <HelpTooltip content="The type of investment: Stock (individual company shares), ETF (exchange-traded fund), Crypto (cryptocurrency), Bond, Mutual Fund, Precious Metal (gold/silver), Currency (forex), Money Market Fund, or Other." />
                    </div>
                    <select
                      value={assetForm.asset_type}
                      onChange={(e) => setAssetForm({ ...assetForm, asset_type: e.target.value })}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="stock">Stock</option>
                      <option value="etf">ETF</option>
                      <option value="crypto">Cryptocurrency</option>
                      <option value="bond">Bond</option>
                      <option value="mutual_fund">Mutual Fund</option>
                      <option value="precious_metal">Precious Metal (Gold/Silver/Platinum)</option>
                      <option value="currency">Currency / Foreign Exchange</option>
                      <option value="money_market">Money Market Fund</option>
                      <option value="commodity">Commodity</option>
                      <option value="other">Other</option>
                    </select>
                  </div>

                  <div>
                    <div className="flex items-center mb-2">
                      <label className="block text-sm font-medium text-slate-700">Category *</label>
                      <HelpTooltip content="Which portfolio category this belongs to: Stock & ETF (stocks and ETFs), CIC (bonds and mutual funds), Foundation, Crypto, Currency & Metals (precious metals and forex), or Other." />
                    </div>
                    <select
                      value={assetForm.asset_category}
                      onChange={(e) => setAssetForm({ ...assetForm, asset_category: e.target.value })}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="stock-etf">Stock & ETF</option>
                      <option value="cic">Core Investment Combo (CIC)</option>
                      <option value="foundation">Foundation</option>
                      <option value="crypto">Crypto</option>
                      <option value="currency-metal">Currency & Metals</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">Purchase Date *</label>
                  <input
                    type="datetime-local"
                    value={assetForm.purchase_date}
                    onChange={(e) => setAssetForm({ ...assetForm, purchase_date: e.target.value })}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">Remarks</label>
                  <textarea
                    value={assetForm.remarks}
                    onChange={(e) => setAssetForm({ ...assetForm, remarks: e.target.value })}
                    placeholder="Add any notes or remarks..."
                    rows={3}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div className="flex gap-3 justify-end pt-4">
                  <button
                    type="button"
                    onClick={() => {
                      setShowAddAsset(false);
                      setAutoFillData(null);
                      setAssetForm({
                        symbol: '',
                        name: '',
                        quantity: 0,
                        average_buy_price: 0,
                        asset_type: 'stock',
                        asset_category: 'stock-etf',
                        currency: 'USD',
                        purchase_date: getLocalDateTime(),
                        remarks: '',
                      });
                    }}
                    className="px-4 py-2 text-slate-700 border border-slate-300 rounded-lg hover:bg-slate-50 font-medium transition-all"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition-all"
                  >
                    Add Asset
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Edit Asset Modal */}
        {showEditAsset && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-xl shadow-lg max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
              <div className="flex justify-between items-center p-6 border-b border-slate-200 sticky top-0 bg-white">
                <h2 className="text-xl font-bold text-slate-900">Edit Asset</h2>
                <button
                  onClick={() => {
                    setShowEditAsset(false);
                    setEditingAsset(null);
                    setAssetForm({
                      symbol: '',
                      name: '',
                      quantity: 0,
                      average_buy_price: 0,
                      asset_type: 'stock',
                      asset_category: 'stock-etf',
                      currency: 'USD',
                      purchase_date: getLocalDateTime(),
                      remarks: '',
                    });
                  }}
                  className="text-slate-500 hover:text-slate-700"
                >
                  ✕
                </button>
              </div>

              <form onSubmit={handleUpdateAsset} className="p-6 space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">Symbol *</label>
                  <input
                    type="text"
                    value={assetForm.symbol}
                    onChange={(e) => setAssetForm({ ...assetForm, symbol: e.target.value.toUpperCase() })}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">Name *</label>
                  <input
                    type="text"
                    value={assetForm.name}
                    onChange={(e) => setAssetForm({ ...assetForm, name: e.target.value })}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">Currency *</label>
                  <select
                    value={assetForm.currency}
                    onChange={(e) => setAssetForm({ ...assetForm, currency: e.target.value })}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="USD">USD - US Dollar</option>
                    <option value="HKD">HKD - Hong Kong Dollar</option>
                    <option value="CNY">CNY - Chinese Yuan</option>
                    <option value="EUR">EUR - Euro</option>
                    <option value="GBP">GBP - British Pound</option>
                    <option value="JPY">JPY - Japanese Yen</option>
                    <option value="CAD">CAD - Canadian Dollar</option>
                    <option value="AUD">AUD - Australian Dollar</option>
                  </select>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">Quantity *</label>
                    <input
                      type="number"
                      step="0.01"
                      value={assetForm.quantity}
                      onChange={(e) => setAssetForm({ ...assetForm, quantity: parseFloat(e.target.value) || 0 })}
                      placeholder="0.00"
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">Average Buy Price *</label>
                    <input
                      type="number"
                      step="0.01"
                      value={assetForm.average_buy_price}
                      onChange={(e) => setAssetForm({ ...assetForm, average_buy_price: parseFloat(e.target.value) || 0 })}
                      placeholder="0.00"
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">Asset Type *</label>
                    <select
                      value={assetForm.asset_type}
                      onChange={(e) => setAssetForm({ ...assetForm, asset_type: e.target.value })}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="stock">Stock</option>
                      <option value="etf">ETF</option>
                      <option value="crypto">Cryptocurrency</option>
                      <option value="bond">Bond</option>
                      <option value="mutual_fund">Mutual Fund</option>
                      <option value="precious_metal">Precious Metal (Gold/Silver/Platinum)</option>
                      <option value="currency">Currency / Foreign Exchange</option>
                      <option value="money_market">Money Market Fund</option>
                      <option value="commodity">Commodity</option>
                      <option value="other">Other</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">Category *</label>
                    <select
                      value={assetForm.asset_category}
                      onChange={(e) => setAssetForm({ ...assetForm, asset_category: e.target.value })}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="stock-etf">Stock & ETF</option>
                      <option value="cic">Core Investment Combo (CIC)</option>
                      <option value="foundation">Foundation</option>
                      <option value="crypto">Crypto</option>
                      <option value="currency-metal">Currency & Metals</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">Purchase Date *</label>
                  <input
                    type="datetime-local"
                    value={assetForm.purchase_date}
                    onChange={(e) => setAssetForm({ ...assetForm, purchase_date: e.target.value })}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">Remarks</label>
                  <textarea
                    value={assetForm.remarks}
                    onChange={(e) => setAssetForm({ ...assetForm, remarks: e.target.value })}
                    placeholder="Add any notes or remarks..."
                    rows={3}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div className="flex gap-3 justify-end pt-4">
                  <button
                    type="button"
                    onClick={() => {
                      setShowEditAsset(false);
                      setEditingAsset(null);
                      setAssetForm({
                        symbol: '',
                        name: '',
                        quantity: 0,
                        average_buy_price: 0,
                        asset_type: 'stock',
                        asset_category: 'stock-etf',
                        currency: 'USD',
                        purchase_date: getLocalDateTime(),
                        remarks: '',
                      });
                    }}
                    className="px-4 py-2 text-slate-700 border border-slate-300 rounded-lg hover:bg-slate-50 font-medium transition-all"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition-all"
                  >
                    Update Asset
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Add Transaction Modal */}
        {showAddTransaction && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-xl shadow-lg max-w-lg w-full mx-4">
              <div className="flex justify-between items-center p-6 border-b border-slate-200">
                <h2 className="text-xl font-bold text-slate-900">Add Transaction</h2>
                <button
                  onClick={() => {
                    setShowAddTransaction(false);
                    setTransactionForm({
                      asset_id: 0,
                      transaction_type: 'buy',
                      quantity: 0,
                      price_per_unit: 0,
                      notes: '',
                      transaction_date: getLocalDateTime(),
                    });
                  }}
                  className="text-slate-500 hover:text-slate-700"
                >
                  ✕
                </button>
              </div>

              <form onSubmit={handleAddTransaction} className="p-6 space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">Transaction Type *</label>
                  <select
                    value={transactionForm.transaction_type}
                    onChange={(e) => setTransactionForm({ ...transactionForm, transaction_type: e.target.value as 'buy' | 'sell' })}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="buy">Buy</option>
                    <option value="sell">Sell</option>
                  </select>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">Quantity *</label>
                    <input
                      type="number"
                      step="0.01"
                      value={transactionForm.quantity}
                      onChange={(e) => setTransactionForm({ ...transactionForm, quantity: parseFloat(e.target.value) || 0 })}
                      placeholder="0.00"
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">Price per Unit *</label>
                    <input
                      type="number"
                      step="0.01"
                      value={transactionForm.price_per_unit}
                      onChange={(e) => setTransactionForm({ ...transactionForm, price_per_unit: parseFloat(e.target.value) || 0 })}
                      placeholder="0.00"
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">Transaction Date *</label>
                  <input
                    type="datetime-local"
                    value={transactionForm.transaction_date}
                    onChange={(e) => setTransactionForm({ ...transactionForm, transaction_date: e.target.value })}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">Notes</label>
                  <textarea
                    value={transactionForm.notes}
                    onChange={(e) => setTransactionForm({ ...transactionForm, notes: e.target.value })}
                    placeholder="Add any notes..."
                    rows={3}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div className="flex gap-3 justify-end pt-4">
                  <button
                    type="button"
                    onClick={() => {
                      setShowAddTransaction(false);
                      setTransactionForm({
                        asset_id: 0,
                        transaction_type: 'buy',
                        quantity: 0,
                        price_per_unit: 0,
                        notes: '',
                        transaction_date: getLocalDateTime(),
                      });
                    }}
                    className="px-4 py-2 text-slate-700 border border-slate-300 rounded-lg hover:bg-slate-50 font-medium transition-all"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium transition-all"
                  >
                    Add Transaction
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
