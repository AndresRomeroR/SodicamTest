import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, map } from 'rxjs';
import { environment } from '../../environments/environment';

export interface ApiResponse<T> {
  isSuccessful: boolean;
  isError: boolean;
  errorMessage?: string;
  messages?: string[];
  result: T;
}

export interface PrintRequest {
  lpn: string;
  zone?: string;
  requestedBy?: string;
  reprintReason?: string;
}

export interface PrintResult {
  requestId: string;
  result: 'APPROVED' | 'REJECTED';
  eventType: 'PRINT' | 'REPRINT' | 'REJECTED';
  isReprint: boolean;
  requestedBy?: string;
  zone?: string;
  document?: {
    documentType: string;
    documentNumber: string;
    status: string;
  };
  label?: {
    etqId: string;
    lpnId: string;
    templateCode: string;
    zpl?: string | null;
  };
  products?: Array<{
    productCode: string;
    productDescription: string;
    requestedQty: number;
    uom: string;
  }>;
  rejectionReasons: string[];
  reprintReason?: string | null;
}

export interface HistoryEvent {
  requestId: string;
  timestamp: string;
  requestedBy: string;
  zone: string;
  etqId: string;
  lpnId: string;
  result: 'APPROVED' | 'REJECTED';
  eventType: 'PRINT' | 'REPRINT' | 'REJECTED';
  reasons: string[];
  reprintReason?: string | null;
}

@Injectable({ providedIn: 'root' })
export class LabelPrintService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiUrl}/labels`;

  print(request: PrintRequest): Observable<PrintResult> {
    return this.http
      .post<ApiResponse<PrintResult>>(`${this.baseUrl}/print`, request)
      .pipe(map((response) => response.result));
  }

  history(identifier?: string): Observable<HistoryEvent[]> {
    const params = identifier ? new HttpParams().set('identifier', identifier) : undefined;
    return this.http
      .get<ApiResponse<HistoryEvent[]>>(`${this.baseUrl}/history`, { params })
      .pipe(map((response) => response.result));
  }
}
