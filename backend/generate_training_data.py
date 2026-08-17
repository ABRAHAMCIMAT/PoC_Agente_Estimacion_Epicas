"""
Generate improved synthetic training data for epic estimation.
Creates diverse stories with realistic feature distributions.
"""

import pandas as pd
import numpy as np
import re
from typing import List, Dict

class TrainingDataGenerator:
    def __init__(self, random_seed: int = 42):
        np.random.seed(random_seed)
    
    def generate_stories(self, n_samples: int = 200) -> pd.DataFrame:
        """Generate diverse synthetic stories."""
        
        # Templates for different story types
        story_templates = {
            'simple_ui': {
                'titles': [
                    'Crear pantalla de {feature}',
                    'Diseñar interfaz de {feature}',
                    'Implementar formulario de {feature}',
                    'Agregar botón para {feature}',
                    'Mejorar visualización de {feature}'
                ],
                'features': ['login', 'registro', 'perfil', 'búsqueda', 'listado', 'contacto'],
                'complexity': 0.3,
                'scope': 'small'
            },
            'complex_backend': {
                'titles': [
                    'Implementar sistema de {feature}',
                    'Desarrollar API de {feature}',
                    'Integrar {feature} con base de datos',
                    'Crear servicio de {feature}',
                    'Optimizar {feature} para rendimiento'
                ],
                'features': ['autenticación', 'pagos', 'reportes', 'notificaciones', 'caché', 'sincronización'],
                'complexity': 0.7,
                'scope': 'large'
            },
            'integration': {
                'titles': [
                    'Integrar API de {feature}',
                    'Conectar con {feature} externo',
                    'Sincronizar datos de {feature}',
                    'Implementar webhook para {feature}',
                    'Migrar datos de {feature}'
                ],
                'features': ['Stripe', 'Twilio', 'SendGrid', 'Firebase', 'AWS', 'terceros'],
                'complexity': 0.8,
                'scope': 'large'
            },
            'bug_fix': {
                'titles': [
                    'Corregir bug en {feature}',
                    'Arreglar error de {feature}',
                    'Solucionar problema en {feature}',
                    'Parchar vulnerabilidad en {feature}',
                    'Ajustar comportamiento de {feature}'
                ],
                'features': ['validación', 'permisos', 'performance', 'seguridad', 'manejo de errores'],
                'complexity': 0.4,
                'scope': 'small'
            },
            'testing': {
                'titles': [
                    'Crear tests para {feature}',
                    'Agregar cobertura de tests a {feature}',
                    'Implementar tests de {feature}',
                    'Validar {feature} con QA',
                    'Escribir tests de integración para {feature}'
                ],
                'features': ['módulo de pagos', 'autenticación', 'API', 'reportes', 'formularios'],
                'complexity': 0.5,
                'scope': 'medium'
            }
        }
        
        stories = []
        story_type_list = list(story_templates.keys())
        
        for i in range(n_samples):
            # Choose random story type
            story_type = np.random.choice(story_type_list)
            template = story_templates[story_type]
            
            # Generate story
            title_template = np.random.choice(template['titles'])
            feature = np.random.choice(template['features'])
            title = title_template.format(feature=feature)
            
            # Generate description based on story type and complexity
            description = self._generate_description(
                title, 
                story_type,
                template['complexity'],
                template['scope']
            )
            
            # Generate acceptance criteria
            criteria = self._generate_criteria(story_type, template['complexity'])
            criteria_str = '\n'.join(criteria)
            
            # Calculate targets based on story characteristics
            points = self._estimate_points(template['complexity'], len(criteria), len(description))
            duration = self._estimate_duration(points)
            cost = self._estimate_cost(points, duration)
            effort = self._estimate_effort(points, template['complexity'])
            
            stories.append({
                'Titulo': title,
                'Historia de Usuario': description,
                'Criterios de Aceptación': criteria_str,
                'Custom field (Story Points)': points,
                'Duracion_Sprint': duration,
                'Costo_por_dia': cost,
                'Esfuerzo_por_Puntos_Historia': effort
            })
        
        return pd.DataFrame(stories)
    
    def _generate_description(self, title: str, story_type: str, complexity: float, scope: str) -> str:
        """Generate realistic story description."""
        
        descriptions = {
            'simple_ui': [
                'Se necesita crear una interfaz de usuario intuitiva que permita a los usuarios {action}. El diseño debe ser responsive y compatible con dispositivos móviles.',
                'Implementar un {action} que sea fácil de usar y accesible. Incluir validación en tiempo real y mensajes de error claros.',
                'Desarrollar componente visual para {action}. Debe incluir estilos consistentes con el design system.',
            ],
            'complex_backend': [
                'Diseñar e implementar arquitectura robusta para {action}. Incluir manejo de errores, logging y monitoreo. Optimizar para escalabilidad.',
                'Crear sistema de {action} con soporte para múltiples proveedores. Implementar caché para optimizar rendimiento y reducir latencia.',
                'Desarrollar servicio de {action} con autenticación y autorización. Incluir validación de datos y manejo de excepciones.',
            ],
            'integration': [
                'Integrar plataforma externa de {action} con nuestra aplicación. Implementar manejo robusto de errores y reintentos automáticos.',
                'Conectar API de {action} y sincronizar datos en tiempo real. Incluir webhooks para notificaciones de eventos.',
                'Implementar proceso de sincronización bidireccional con {action}. Manejar conflictos de datos y consistencia.',
            ],
            'bug_fix': [
                'Investigar y corregir problema reportado en {action}. Agregar tests para prevenir regresión.',
                'Solucionar issue de {action} que afecta experiencia del usuario. Implementar validación adicional.',
                'Arreglar vulnerabilidad de {action}. Realizar auditoría de seguridad y aplicar parches.',
            ],
            'testing': [
                'Crear suite completa de tests para {action}. Incluir tests unitarios, de integración y end-to-end.',
                'Agregar cobertura de tests a {action} para alcanzar 80%+ de cobertura. Documentar casos de prueba.',
                'Implementar tests de rendimiento para {action}. Validar bajo carga alta.',
            ]
        }
        
        action_map = {
            'simple_ui': 'permite a los usuarios ingresar información',
            'complex_backend': 'procesa datos y genera reportes',
            'integration': 'comunica con sistemas externos',
            'bug_fix': 'se valida correctamente la entrada',
            'testing': 'funciona correctamente en todos los casos'
        }
        
        base_desc = np.random.choice(descriptions.get(story_type, descriptions['simple_ui']))
        full_desc = base_desc.format(action=action_map.get(story_type, 'funciona'))
        
        # Add complexity-dependent details
        if complexity > 0.7:
            full_desc += ' Requerirá análisis detallado, diseño de arquitectura y múltiples iteraciones de implementación.'
        elif complexity > 0.5:
            full_desc += ' Incluye múltiples componentes y requiere coordinación entre equipos.'
        else:
            full_desc += ' Tarea de alcance limitado y bien definida.'
        
        return full_desc
    
    def _generate_criteria(self, story_type: str, complexity: float) -> List[str]:
        """Generate acceptance criteria."""
        
        base_criteria = {
            'simple_ui': [
                'La interfaz debe ser responsive y funcionar en dispositivos móviles',
                'Debe incluir validación de campos obligatorios',
                'Los mensajes de error deben ser claros y útiles',
                'El diseño debe cumplir con el design system',
            ],
            'complex_backend': [
                'El servicio debe manejar errores de forma robusta',
                'Implementar logging detallado de operaciones',
                'Incluir tests unitarios con cobertura > 80%',
                'Documentar API y casos de uso',
                'Optimizar para rendimiento y escalabilidad',
            ],
            'integration': [
                'La integración debe manejar fallos de conexión',
                'Implementar reintentos automáticos',
                'Incluir webhooks para eventos importantes',
                'Documentar flujo de sincronización',
                'Agregar monitoreo y alertas',
            ],
            'bug_fix': [
                'El bug debe estar completamente resuelto',
                'Agregar tests para prevenir regresión',
                'Validar en múltiples navegadores/dispositivos',
            ],
            'testing': [
                'Cobertura de tests > 80%',
                'Tests deben pasar en CI/CD',
                'Documentar escenarios de prueba',
                'Incluir tests de caso límite',
            ]
        }
        
        criteria = base_criteria.get(story_type, base_criteria['simple_ui']).copy()
        
        # Add extra criteria based on complexity
        if complexity > 0.8:
            criteria.append('Realizar revisión de seguridad')
            criteria.append('Validar rendimiento bajo carga')
        
        if complexity > 0.6:
            criteria.append('Incluir documentación técnica')
        
        return criteria[:max(2, int(2 + complexity * 3))]
    
    def _estimate_points(self, complexity: float, criteria_count: int, desc_length: int) -> float:
        """Estimate story points realistically."""
        
        # Base points on complexity
        base_points = 1 + complexity * 12
        
        # Adjust by criteria count
        criteria_adjustment = (criteria_count - 1) * 0.5
        
        # Adjust by description length
        length_adjustment = min(desc_length / 200, 2) * 0.5
        
        points = base_points + criteria_adjustment + length_adjustment
        
        # Add some randomness
        points += np.random.normal(0, 0.5)
        
        # Fibonacci sequence (1, 2, 3, 5, 8, 13)
        fibonacci = [1, 2, 3, 5, 8, 13]
        closest = min(fibonacci, key=lambda x: abs(x - points))
        
        return max(1, float(closest))
    
    def _estimate_duration(self, points: float) -> float:
        """Estimate sprint duration in days."""
        
        # Linear relationship: more points = more days
        duration = 0.5 + (points / 2.0)
        
        # Add randomness
        duration += np.random.normal(0, 0.8)
        
        return max(0.5, float(duration))
    
    def _estimate_cost(self, points: float, duration: float) -> float:
        """Estimate cost in dollars."""
        
        # Assume $200/day developer rate
        daily_rate = 200
        
        cost = daily_rate * duration
        
        # Add randomness
        cost += np.random.normal(0, 100)
        
        return max(100, float(cost))
    
    def _estimate_effort(self, points: float, complexity: float) -> float:
        """Estimate effort in hours."""
        
        # Base: ~12 hours per story point
        effort = points * 12
        
        # Complexity multiplier
        effort *= (0.8 + complexity * 0.4)
        
        # Add randomness
        effort += np.random.normal(0, 8)
        
        return max(4, float(effort))


def main():
    """Generate and save training data."""
    
    print("Generating improved training data...")
    generator = TrainingDataGenerator(random_seed=42)
    
    # Generate 150 diverse stories
    df = generator.generate_stories(n_samples=150)
    
    # Save to CSV
    output_file = 'training_data_improved.csv'
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\n[OK] Generated {len(df)} training samples")
    print(f"[OK] Saved to {output_file}")
    
    # Print statistics
    print("\nDataset Statistics:")
    print(f"  Story Points: {df['Custom field (Story Points)'].min():.1f} - {df['Custom field (Story Points)'].max():.1f} (avg: {df['Custom field (Story Points)'].mean():.1f})")
    print(f"  Duration (days): {df['Duracion_Sprint'].min():.1f} - {df['Duracion_Sprint'].max():.1f} (avg: {df['Duracion_Sprint'].mean():.1f})")
    print(f"  Cost: ${df['Costo_por_dia'].min():.0f} - ${df['Costo_por_dia'].max():.0f} (avg: ${df['Costo_por_dia'].mean():.0f})")
    print(f"  Effort: {df['Esfuerzo_por_Puntos_Historia'].min():.1f} - {df['Esfuerzo_por_Puntos_Historia'].max():.1f} hours (avg: {df['Esfuerzo_por_Puntos_Historia'].mean():.1f})")
    
    print("\nSample stories:")
    print(df[['Titulo', 'Custom field (Story Points)']].head(10))


if __name__ == '__main__':
    main()
