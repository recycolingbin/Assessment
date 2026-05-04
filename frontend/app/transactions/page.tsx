'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { transactionsAPI, assetsAPI } from '@/lib/api';

interface Transaction {
  id: number;
  asset_id: number;
  transaction_type: 'buy' | 'sell';
  quantity: number;
  price_per_unit: number;
  total_value: number;
  notes: string;
  transaction_date: string;
  created_at: string;
  asset?: {
    symbol: string;
    name: string;
    currency: string;
  };
}

export default function TransactionsPage() {
  const router = useRouter();
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);
  const [limit] = useState(50);
  const [hasMore, setHasMore] = useState(true);
  const [filterType, setFilterType] = useState<'all' | 'buy' | 'sell'>('all');
  const [searchSymbol, setSearchSymbol] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }
    fetchTransactions();
  }, [router, page]);

  const fetchTransactions = async () => {
    try {
      setLoading(true);
      const response = await transactionsAPI.getAll(page * limit, limit);
      const newTransactions = response.data;

      // Fetch asset details for each transaction
      const transactionsWithAssets = await Promise.all(
        newTransactions.map(async (transaction: Transaction) => {
          try {
            const assetResponse = await assetsAPI.getById(transaction.asset_id);
            return { ...transaction, asset: assetResponse.data };
          } catch (error) {
            return transaction;
          }
        })
      );

      setTransactions(transactionsWithAssets);
      setHasMore(newTransactions.length === limit);
    } catch (error) {
      console.error('Error fetching transactions:', error);
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

  const filteredTransactions = transactions.filter((transaction) => {
    const matchesType = filterType === 'all' || transaction.transaction_type === filterType;
    const matchesSymbol = searchSymbol === '' || transaction.asset?.symbol.toLowerCase().includes(searchSymbol.toLowerCase());
    return matchesType && matchesSymbol;
  });

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

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="text-center">
          <div className="inline-block w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
          <p className="mt-4 text-slate-600 font-medium">Loading transactions...</p>
        </div>
      </div>
    );
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
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <div>
                <h1 className="text-xl font-bold text-slate-900">Transaction History</h1>
                <p className="text-xs text-slate-500">View all buy and sell transactions</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={() => router.push('/dashboard')}
                className="px-4 py-2 text-slate-700 hover:text-slate-900 font-medium transition-colors"
              >
                Dashboard
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
        {/* Filters */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Filter by Type</label>
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value as 'all' | 'buy' | 'sell')}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">All Transactions</option>
                <option value="buy">Buy Only</option>
                <option value="sell">Sell Only</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Search by Symbol</label>
              <input
                type="text"
                value={searchSymbol}
                onChange={(e) => setSearchSymbol(e.target.value)}
                placeholder="e.g., AAPL, BTC"
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>

        {/* Transactions Table */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-50">
                <tr className="border-b border-slate-200">
                  <th className="text-left py-3 px-4 font-semibold text-slate-700">Date</th>
                  <th className="text-left py-3 px-4 font-semibold text-slate-700">Type</th>
                  <th className="text-left py-3 px-4 font-semibold text-slate-700">Symbol</th>
                  <th className="text-left py-3 px-4 font-semibold text-slate-700">Asset Name</th>
                  <th className="text-right py-3 px-4 font-semibold text-slate-700">Quantity</th>
                  <th className="text-right py-3 px-4 font-semibold text-slate-700">Price/Unit</th>
                  <th className="text-right py-3 px-4 font-semibold text-slate-700">Total Value</th>
                  <th className="text-left py-3 px-4 font-semibold text-slate-700">Notes</th>
                </tr>
              </thead>
              <tbody>
                {filteredTransactions.length > 0 ? (
                  filteredTransactions.map((transaction) => (
                    <tr key={transaction.id} className="border-b border-slate-100 hover:bg-slate-50">
                      <td className="py-3 px-4 text-slate-700">
                        {new Date(transaction.transaction_date).toLocaleDateString()}
                      </td>
                      <td className="py-3 px-4">
                        <span
                          className={`px-2 py-1 rounded-full text-xs font-semibold ${
                            transaction.transaction_type === 'buy'
                              ? 'bg-green-100 text-green-700'
                              : 'bg-red-100 text-red-700'
                          }`}
                        >
                          {transaction.transaction_type.toUpperCase()}
                        </span>
                      </td>
                      <td className="py-3 px-4 font-semibold text-slate-900">
                        {transaction.asset?.symbol || 'N/A'}
                      </td>
                      <td className="py-3 px-4 text-slate-700">
                        {transaction.asset?.name || 'Unknown Asset'}
                      </td>
                      <td className="py-3 px-4 text-right text-slate-900">
                        {transaction.quantity}
                      </td>
                      <td className="py-3 px-4 text-right text-slate-900">
                        {formatCurrency(transaction.price_per_unit, transaction.asset?.currency)}
                      </td>
                      <td className="py-3 px-4 text-right font-semibold text-slate-900">
                        {formatCurrency(transaction.total_value, transaction.asset?.currency)}
                      </td>
                      <td className="py-3 px-4 text-slate-600 text-xs">
                        {transaction.notes || '-'}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={8} className="py-8 text-center text-slate-400">
                      No transactions found
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {filteredTransactions.length > 0 && (
            <div className="flex justify-between items-center p-4 border-t border-slate-200">
              <button
                onClick={() => setPage(Math.max(0, page - 1))}
                disabled={page === 0}
                className="px-4 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              <span className="text-sm text-slate-600">Page {page + 1}</span>
              <button
                onClick={() => setPage(page + 1)}
                disabled={!hasMore}
                className="px-4 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
