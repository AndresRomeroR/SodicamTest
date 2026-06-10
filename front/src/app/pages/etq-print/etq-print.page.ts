import { CommonModule } from '@angular/common';
import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { finalize } from 'rxjs';
import { HistoryEvent, LabelPrintService, PrintResult } from '../../services/label-print.service';

@Component({
  selector: 'app-etq-print-page',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './etq-print.page.html',
  styleUrl: './etq-print.page.scss'
})
export class EtqPrintPage implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly labelPrintService = inject(LabelPrintService);

  protected readonly form = this.fb.nonNullable.group({
    lpn: ['olpn12345', [Validators.required]],
    zone: ['ZONA-PICKING-A'],
    requestedBy: ['usuario.operacion'],
    reprintReason: ['']
  });

  protected readonly loading = signal(false);
  protected readonly historyLoading = signal(false);
  protected readonly result = signal<PrintResult | null>(null);
  protected readonly history = signal<HistoryEvent[]>([]);
  protected readonly error = signal<string | null>(null);
  protected readonly zones = ['ZONA-PICKING-A', 'ZONA-PICKING-B'];

  protected readonly approvedCount = computed(() => this.history().filter((event) => event.result === 'APPROVED').length);
  protected readonly rejectedCount = computed(() => this.history().filter((event) => event.result === 'REJECTED').length);
  protected readonly reprintCount = computed(() => this.history().filter((event) => event.eventType === 'REPRINT').length);

  ngOnInit(): void {
    this.loadHistory();
  }

  protected submit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.loading.set(true);
    this.error.set(null);
    this.result.set(null);

    this.labelPrintService
      .print(this.form.getRawValue())
      .pipe(finalize(() => this.loading.set(false)))
      .subscribe({
        next: (result) => {
          this.result.set(result);
          this.loadHistory(this.form.controls.lpn.value);
        },
        error: (error) => {
          this.error.set(error?.error?.detail ?? 'No fue posible procesar la solicitud');
        }
      });
  }

  protected loadHistory(identifier = ''): void {
    this.historyLoading.set(true);
    this.labelPrintService
      .history(identifier.trim() || undefined)
      .pipe(finalize(() => this.historyLoading.set(false)))
      .subscribe({
        next: (history) => this.history.set(history),
        error: () => this.history.set([])
      });
  }
}
