#!/usr/bin/env python3
"""
CARBONICA Command Line Interface Main Entry Point
"""

import sys
import argparse
from typing import List, Optional

from carbonica import CARBONICA
from carbonica.cli.commands import (
    init_command, download_command, process_command,
    pcsi_command, serve_command, plot_command,
    export_command, validate_command
)


def create_parser() -> argparse.ArgumentParser:
    """Create main argument parser"""
    parser = argparse.ArgumentParser(
        description='🌍 CARBONICA - Planetary Carbon Accounting Framework',
        epilog='For more information, visit https://carbonica.netlify.app'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='CARBONICA 1.0.0 (DOI: 10.5281/zenodo.18995446)'
    )
    
    parser.add_argument(
        '--data-dir', '-d',
        default='./data',
        help='Data directory path (default: ./data)'
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(
        title='commands',
        dest='command',
        required=True
    )
    
    # Init command
    init_parser = subparsers.add_parser(
        'init',
        help='Initialize CARBONICA project'
    )
    init_parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='Force overwrite existing files'
    )
    
    # Download command
    download_parser = subparsers.add_parser(
        'download',
        help='Download observational data'
    )
    download_parser.add_argument(
        '--source', '-s',
        choices=['keeling', 'socat', 'gcp', 'gtnp', 'glodap', 'modis', 'gosat', 'oco2', 'all'],
        default='all',
        help='Data source to download'
    )
    download_parser.add_argument(
        '--year', '-y',
        type=int,
        help='Specific year to download'
    )
    
    # Process command
    process_parser = subparsers.add_parser(
        'process',
        help='Process data and compute parameters'
    )
    process_parser.add_argument(
        '--year', '-y',
        type=int,
        default=2025,
        help='Target year (default: 2025)'
    )
    process_parser.add_argument(
        '--ensemble', '-e',
        type=int,
        default=10000,
        help='Monte Carlo ensemble size (default: 10000)'
    )
    process_parser.add_argument(
        '--output', '-o',
        default='./results',
        help='Output directory (default: ./results)'
    )
    
    # PCSI command
    pcsi_parser = subparsers.add_parser(
        'pcsi',
        help='Compute Planetary Carbon Saturation Index'
    )
    pcsi_parser.add_argument(
        '--year', '-y',
        type=int,
        default=2025,
        help='Target year (default: 2025)'
    )
    pcsi_parser.add_argument(
        '--scenario', '-s',
        choices=['SSP1-1.9', 'SSP3-7.0', 'SSP5-8.5'],
        help='Projection scenario'
    )
    pcsi_parser.add_argument(
        '--end-year',
        type=int,
        default=2070,
        help='Projection end year (default: 2070)'
    )
    
    # Serve command
    serve_parser = subparsers.add_parser(
        'serve',
        help='Start web dashboard server'
    )
    serve_parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Host address (default: 127.0.0.1)'
    )
    serve_parser.add_argument(
        '--port', '-p',
        type=int,
        default=5000,
        help='Port number (default: 5000)'
    )
    serve_parser.add_argument(
        '--debug',
        action='store_true',
        help='Run in debug mode'
    )
    
    # Plot command
    plot_parser = subparsers.add_parser(
        'plot',
        help='Generate plots'
    )
    plot_parser.add_argument(
        '--type', '-t',
        choices=['timeseries', 'correlation', 'projection', 'parameters', 'all'],
        default='all',
        help='Plot type'
    )
    plot_parser.add_argument(
        '--output', '-o',
        default='./figures',
        help='Output directory (default: ./figures)'
    )
    plot_parser.add_argument(
        '--format', '-f',
        choices=['txt', 'csv', 'json'],
        default='txt',
        help='Output format (default: txt)'
    )
    
    # Export command
    export_parser = subparsers.add_parser(
        'export',
        help='Export results'
    )
    export_parser.add_argument(
        '--format', '-f',
        choices=['csv', 'json', 'netcdf'],
        default='csv',
        help='Export format (default: csv)'
    )
    export_parser.add_argument(
        '--output', '-o',
        default='./results',
        help='Output directory (default: ./results)'
    )
    
    # Validate command
    validate_parser = subparsers.add_parser(
        'validate',
        help='Validate against observations'
    )
    validate_parser.add_argument(
        '--test',
        choices=['keeling', 'revelle', 'permafrost', 'npp', 'all'],
        default='all',
        help='Validation test'
    )
    
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    # Create CARBONICA instance
    carbonica = CARBONICA(data_dir=args.data_dir)
    
    # Execute command
    if args.command == 'init':
        return init_command(args, carbonica)
    elif args.command == 'download':
        return download_command(args, carbonica)
    elif args.command == 'process':
        return process_command(args, carbonica)
    elif args.command == 'pcsi':
        return pcsi_command(args, carbonica)
    elif args.command == 'serve':
        return serve_command(args, carbonica)
    elif args.command == 'plot':
        return plot_command(args, carbonica)
    elif args.command == 'export':
        return export_command(args, carbonica)
    elif args.command == 'validate':
        return validate_command(args, carbonica)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
