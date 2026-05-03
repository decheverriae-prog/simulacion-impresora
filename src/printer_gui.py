"""Interfaz gráfica (Tkinter). La lógica de simulación está en los módulos importados."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from .print_simulation import PrintSimulation
from .print_task import PrintTask


class PrinterSimulationApp(ttk.Frame):
    def __init__(self, master: tk.Tk | None = None) -> None:
        super().__init__(master, padding=12)
        self.master.title("Simulación de cola de impresión")
        self.master.minsize(720, 480)
        self.pack(fill=tk.BOTH, expand=True)

        top = ttk.Frame(self)
        top.pack(fill=tk.X)

        ttk.Label(top, text="Segundos por página:").grid(row=0, column=0, sticky=tk.W, padx=(0, 8), pady=4)
        self.seconds_var = tk.StringVar(value="2")
        ttk.Entry(top, textvariable=self.seconds_var, width=10).grid(row=0, column=1, sticky=tk.W, pady=4)

        btns = ttk.Frame(self)
        btns.pack(fill=tk.X, pady=(8, 0))
        ttk.Button(btns, text="Ejemplo rápido", command=self._load_demo).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btns, text="Añadir fila", command=self._add_row).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btns, text="Quitar selección", command=self._remove_selected).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btns, text="Limpiar trabajos", command=self._clear_jobs).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btns, text="Ejecutar simulación", command=self._run_simulation).pack(side=tk.LEFT)

        tbl_frame = ttk.Frame(self)
        tbl_frame.pack(fill=tk.BOTH, expand=True, pady=(12, 0))

        cols = ("id", "pages", "arrival")
        self.tree = ttk.Treeview(tbl_frame, columns=cols, show="headings", height=12, selectmode=tk.BROWSE)
        self.tree.heading("id", text="ID trabajo")
        self.tree.heading("pages", text="Páginas")
        self.tree.heading("arrival", text="Llegada (s)")
        self.tree.column("id", width=160)
        self.tree.column("pages", width=100, anchor=tk.CENTER)
        self.tree.column("arrival", width=120, anchor=tk.CENTER)
        scroll = ttk.Scrollbar(tbl_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.out = tk.Text(self, height=14, wrap=tk.WORD, state=tk.DISABLED)
        self.out.pack(fill=tk.BOTH, expand=True, pady=(12, 0))

        self._load_demo()

    def _append_log(self, text: str) -> None:
        self.out.configure(state=tk.NORMAL)
        self.out.insert(tk.END, text)
        self.out.see(tk.END)
        self.out.configure(state=tk.DISABLED)

    def _clear_log(self) -> None:
        self.out.configure(state=tk.NORMAL)
        self.out.delete("1.0", tk.END)
        self.out.configure(state=tk.DISABLED)

    def _load_demo(self) -> None:
        for i in self.tree.get_children():
            self.tree.delete(i)
        demos = [
            ("T1", "5", "0"),
            ("T2", "3", "4"),
            ("T3", "8", "6"),
            ("T4", "2", "10"),
            ("T5", "4", "12"),
        ]
        for row in demos:
            self.tree.insert("", tk.END, values=row)

    def _add_row(self) -> None:
        self.tree.insert("", tk.END, values=("Nuevo", "1", "0"))

    def _remove_selected(self) -> None:
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Selección", "Seleccione una fila para quitar.")
            return
        for s in sel:
            self.tree.delete(s)

    def _clear_jobs(self) -> None:
        for i in self.tree.get_children():
            self.tree.delete(i)

    def _parse_jobs(self) -> tuple[list[PrintTask], list[str]]:
        tasks: list[PrintTask] = []
        errors: list[str] = []
        for iid in self.tree.get_children():
            vid, pages_s, arrival_s = self.tree.item(iid, "values")
            row_label = str(vid)
            try:
                pages = int(str(pages_s).strip())
            except ValueError:
                errors.append(f"Fila '{row_label}': páginas no numéricas.")
                continue
            try:
                arrival = float(str(arrival_s).strip().replace(",", "."))
            except ValueError:
                errors.append(f"Fila '{row_label}': llegada no numérica.")
                continue
            tasks.append(PrintTask(task_id=str(vid).strip(), pages=pages, arrival_time=arrival))
        return tasks, errors

    def _run_simulation(self) -> None:
        self._clear_log()
        spp_s = self.seconds_var.get().strip().replace(",", ".")
        try:
            spp = float(spp_s)
        except ValueError:
            messagebox.showerror("Entrada", "Segundos por página debe ser un número válido.")
            self._append_log("Error: segundos por página inválido.\n")
            return

        if spp <= 0:
            messagebox.showerror("Validación", "Segundos por página debe ser mayor que cero.")
            self._append_log("Error: segundos por página debe ser positivo.\n")
            return

        tasks, parse_errors = self._parse_jobs()
        for e in parse_errors:
            self._append_log(e + "\n")

        try:
            sim = PrintSimulation(seconds_per_page=spp)
            result = sim.run(tasks)
        except ValueError as ex:
            messagebox.showerror("Error", str(ex))
            self._append_log(str(ex) + "\n")
            return

        for msg in result.rejected:
            self._append_log("Rechazado: " + msg + "\n")

        self._append_log("\n--- Resultados ---\n")
        m = result.metrics
        self._append_log(f"Trabajos procesados (válidos): {m.total_processed}\n")
        self._append_log(f"Tiempo promedio de espera: {m.average_wait_time:.3f} s\n")
        if m.task_id_max_wait is not None:
            self._append_log(
                f"Mayor tiempo de espera: {m.max_wait_time:.3f} s (trabajo {m.task_id_max_wait})\n"
            )
        else:
            self._append_log("Mayor tiempo de espera: N/A (sin trabajos válidos)\n")
        self._append_log(f"Tamaño máximo de la cola: {m.max_queue_size}\n")

        if result.completed:
            self._append_log("\nDetalle por trabajo:\n")
            for c in result.completed:
                self._append_log(
                    f"  {c.task.task_id}: espera={c.wait_time:.3f}s, "
                    f"servicio [{c.service_start:.3f} – {c.service_end:.3f}] s\n"
                )

        self._append_log("\n")


def launch_app() -> None:
    root = tk.Tk()
    try:
        root.call("tk", "scaling", 1.25)
    except tk.TclError:
        pass
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")
    PrinterSimulationApp(master=root)
    root.mainloop()
