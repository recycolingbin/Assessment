'use client';

import { useEffect, useState } from 'react';
import { transactionsAPI } from '@/lib/api';
import { exportTransactionToPDF } from '@/lib/pdfExport';

interface TransactionDetailModalProps {
  transactionId: number;
  onClose: () => void;
}

export default function TransactionDetailModal({ transactionId, onClose }: TransactionDetailModalProps) {
  const [transaction, setTransaction] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTransaction = async () => {
      try {
        const response = await transactionsAPI.getById(transactionId);
        setTransaction(response.data);
      } catch (error) {
        console.error('Error fetching transaction:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTransaction();
  }, [transactionId]);

  const handleExportPDF = () => {
    if (transaction) {
      exportTransactionToPDF(transaction);
    }
  };

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-2xl w-full">
          <div className="flex items-center justify-center">
            <div className="w-12 h-12 border-4 border-slate-300 border-t-blue-600 rounded-full animate-spin"></div>
          </div>
        </div>
      </div>
    );
  }

  if (!transaction) {
    return (
      <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-2xl w-full">
          <p className="text-center text-slate-600">Transaction not found</p>
          <button
            onClick={onClose}
            className="mt-4 w-full py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 transition-all"
          >
            Close
          </button>
        </div>
      </div>
    );
  }

  const transactionDate = new Date(transaction.transaction_date);
  const isBuy = transaction.transaction_type === 'buy';

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div
        className="bg-white rounded-2xl shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-slate-900 to-slate-800 px-8 py-6 rounded-t-2xl">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-white">Transaction Details</h2>
              <p className="text-slate-300 text-sm mt-1">ID: #{transaction.id}</p>
            </div>
            <button
              onClick={onClose}
              className="text-slate-300 hover:text-white transition-colors p-2"
              aria-label="Close modal"
            >
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-8 space-y-6">
          {/* Transaction Type Badge */}
          <div className="flex items-center gap-3">
            <span className={`inline-flex items-center px-4 py-2 rounded-lg font-semibold text-sm ${
              isBuy
                ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                : 'bg-rose-50 text-rose-700 border border-rose-200'
            }`}>
              {isBuy ? (
                <svg className="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 11l5-5m0 0l5 5m-5-5v12" />
                </svg>
              ) : (
                <svg className="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 13l-5 5m0 0l-5-5m5 5V6" />
                </svg>
              )}
              {transaction.transaction_type.toUpperCase()}
            </span>
            <span className="text-slate-500 text-sm">
              {transactionDate.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
              })}
            </span>
          </div>

          {/* Asset Information */}
          {transaction.asset && (
            <div className="bg-slate-50 rounded-xl p-6 border border-slate-200">
              <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-3">Asset Information</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">Symbol</span>
                  <span className="font-bold text-slate-900 text-lg">{transaction.asset.symbol}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">Name</span>
                  <span className="font-medium text-slate-900">{transaction.asset.name}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">Type</span>
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-700">
                    {transaction.asset.asset_type}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Transaction Details */}
          <div className="bg-white rounded-xl p-6 border border-slate-200">
            <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-4">Transaction Details</h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center py-3 border-b border-slate-100">
                <span className="text-slate-600">Quantity</span>
                <span className="font-semibold text-slate-900">{transaction.quantity.toFixed(4)}</span>
              </div>
              <div className="flex justify-between items-center py-3 border-b border-slate-100">
                <span className="text-slate-600">Price per Unit</span>
                <span className="font-semibold text-slate-900">${transaction.price_per_unit.toFixed(2)}</span>
              </div>
              <div className="flex justify-between items-center py-3 bg-slate-50 -mx-6 px-6 rounded-lg">
                <span className="text-slate-900 font-semibold">Total Amount</span>
                <span className="text-2xl font-bold text-slate-900">${transaction.total_amount.toFixed(2)}</span>
              </div>
            </div>
          </div>

          {/* Notes */}
          {transaction.notes && (
            <div className="bg-amber-50 rounded-xl p-6 border border-amber-200">
              <h3 className="text-sm font-semibold text-amber-900 uppercase tracking-wide mb-2">Notes</h3>
              <p className="text-amber-800">{transaction.notes}</p>
            </div>
          )}
        </div>

        {/* Footer Actions */}
        <div className="bg-slate-50 px-8 py-6 rounded-b-2xl flex gap-3">
          <button
            onClick={handleExportPDF}
            className="flex-1 flex items-center justify-center gap-2 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-all shadow-sm"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Export PDF
          </button>
          <button
            onClick={onClose}
            className="flex-1 py-3 bg-white text-slate-700 font-semibold rounded-lg hover:bg-slate-100 transition-all border border-slate-300"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
