import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

interface TransactionDetail {
  id: number;
  transaction_type: string;
  quantity: number;
  price_per_unit: number;
  total_amount: number;
  transaction_date: string;
  notes?: string;
  asset?: {
    symbol: string;
    name: string;
    asset_type: string;
  };
}

export const exportTransactionToPDF = (transaction: TransactionDetail, userName?: string) => {
  const doc = new jsPDF();

  // Header
  doc.setFillColor(15, 23, 42); // Navy
  doc.rect(0, 0, 210, 40, 'F');

  doc.setTextColor(255, 255, 255);
  doc.setFontSize(24);
  doc.setFont('helvetica', 'bold');
  doc.text('Transaction Report', 20, 25);

  doc.setFontSize(10);
  doc.setFont('helvetica', 'normal');
  doc.text(`Generated: ${new Date().toLocaleString()}`, 20, 33);

  // Reset text color
  doc.setTextColor(0, 0, 0);

  // Transaction Details Section
  let yPos = 55;

  doc.setFontSize(16);
  doc.setFont('helvetica', 'bold');
  doc.text('Transaction Details', 20, yPos);

  yPos += 10;

  // Transaction info table
  const transactionData = [
    ['Transaction ID', `#${transaction.id}`],
    ['Type', transaction.transaction_type.toUpperCase()],
    ['Date', new Date(transaction.transaction_date).toLocaleString()],
    ['Asset Symbol', transaction.asset?.symbol || 'N/A'],
    ['Asset Name', transaction.asset?.name || 'N/A'],
    ['Asset Type', transaction.asset?.asset_type || 'N/A'],
    ['Quantity', transaction.quantity.toFixed(4)],
    ['Price per Unit', `$${transaction.price_per_unit.toFixed(2)}`],
    ['Total Amount', `$${transaction.total_amount.toFixed(2)}`],
  ];

  if (transaction.notes) {
    transactionData.push(['Notes', transaction.notes]);
  }

  autoTable(doc, {
    startY: yPos,
    head: [],
    body: transactionData,
    theme: 'plain',
    styles: {
      fontSize: 11,
      cellPadding: 5,
    },
    columnStyles: {
      0: { fontStyle: 'bold', cellWidth: 50, textColor: [71, 85, 105] },
      1: { cellWidth: 120, textColor: [15, 23, 42] },
    },
  });

  // Footer
  const pageCount = doc.getNumberOfPages();
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i);
    doc.setFontSize(9);
    doc.setTextColor(148, 163, 184);
    doc.text(
      `Page ${i} of ${pageCount}`,
      doc.internal.pageSize.getWidth() / 2,
      doc.internal.pageSize.getHeight() - 10,
      { align: 'center' }
    );

    doc.text(
      'Confidential - For authorized use only',
      20,
      doc.internal.pageSize.getHeight() - 10
    );
  }

  // Save the PDF
  const fileName = `transaction_${transaction.id}_${new Date().toISOString().split('T')[0]}.pdf`;
  doc.save(fileName);
};
